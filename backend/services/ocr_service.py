import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from pathlib import Path

import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
OCR_TIMEOUT_SECONDS = 30


def _validate_image(image_path: str):
    path = Path(image_path)

    if not path.exists():
        return f"File not found: {image_path}"

    if path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        return f"Unsupported file extension: {path.suffix}"

    size = path.stat().st_size
    if size > MAX_FILE_SIZE_BYTES:
        return f"File too large ({size} bytes); limit is {MAX_FILE_SIZE_BYTES} bytes"

    return None


def _run_tesseract(image_path: str) -> str:
    with Image.open(image_path) as image:
        return pytesseract.image_to_string(image)


def extract_layout(image_path: str, timeout: float = OCR_TIMEOUT_SECONDS):
    error = _validate_image(image_path)
    if error:
        logger.error("extract_layout validation failed: %s", error)
        return {"success": False, "error": error}

    executor = ThreadPoolExecutor(max_workers=1)

    try:
        future = executor.submit(_run_tesseract, image_path)
        text = future.result(timeout=timeout)

        logger.info("Extracted %d char(s) from %s", len(text), image_path)
        return {"success": True, "data": text}

    except FutureTimeoutError:
        logger.warning("OCR timed out after %ss for %s", timeout, image_path)
        return {"success": False, "error": f"OCR timed out after {timeout}s", "timed_out": True}

    except Exception as exc:
        logger.exception("OCR failed for %s", image_path)
        return {"success": False, "error": f"OCR failed for {image_path}: {exc}"}

    finally:
        # wait=False: never block on a runaway worker thread — let it be
        # reclaimed in the background once (if ever) it finishes.
        executor.shutdown(wait=False)


def extract_layout_from_images(image_paths: list[str], timeout: float = OCR_TIMEOUT_SECONDS):
    """Run OCR over each page, bounded by an overall time budget.

    If the budget runs out partway through, this stops early and returns
    whatever text was already extracted instead of hanging or failing.
    """
    if not image_paths:
        return {"success": False, "error": "No images provided for OCR"}

    texts = []
    truncated = False
    start = time.monotonic()

    for image_path in image_paths:
        remaining = timeout - (time.monotonic() - start)

        if remaining <= 0:
            logger.warning(
                "OCR time budget (%ss) exhausted after %d/%d page(s); returning partial results",
                timeout, len(texts), len(image_paths),
            )
            truncated = True
            break

        result = extract_layout(image_path, timeout=remaining)

        if result["success"]:
            texts.append(result["data"])
        elif result.get("timed_out"):
            logger.warning(
                "OCR timed out on %s; returning partial results from %d/%d page(s)",
                image_path, len(texts), len(image_paths),
            )
            truncated = True
            break
        else:
            logger.warning("Skipping page %s after OCR error: %s", image_path, result["error"])

    combined_text = "\n".join(t.strip() for t in texts if t.strip())
    return {"success": True, "data": {"text": combined_text}, "truncated": truncated}
