import logging
from pathlib import Path

import easyocr
from pydantic import BaseModel

logger = logging.getLogger(__name__)

reader = easyocr.Reader(['en'])

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


class OCRWord(BaseModel):
    text: str
    bbox: list[list[float]]
    confidence: float


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


def extract_layout(image_path: str):
    error = _validate_image(image_path)
    if error:
        logger.error("extract_layout validation failed: %s", error)
        return {"success": False, "error": error}

    try:
        result = reader.readtext(image_path)

        words = [
            OCRWord(text=text, bbox=bbox, confidence=float(confidence))
            for bbox, text, confidence in result
        ]

        logger.info("Extracted %d word(s) from %s", len(words), image_path)
        return {"success": True, "data": words}

    except Exception as exc:
        logger.exception("OCR failed for %s", image_path)
        return {"success": False, "error": f"OCR failed for {image_path}: {exc}"}


def extract_layout_from_images(image_paths: list[str]):
    if not image_paths:
        return {"success": False, "error": "No images provided for OCR"}

    layouts = []

    for image_path in image_paths:
        result = extract_layout(image_path)
        if not result["success"]:
            return result
        layouts.append(result["data"])

    return {"success": True, "data": layouts}
