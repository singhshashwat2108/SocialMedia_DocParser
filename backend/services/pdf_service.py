import logging
from pathlib import Path

import pymupdf as fitz
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

IMAGE_DIR = Path("converted_images")
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}

MAX_PDF_PAGES = 5
MIN_DIRECT_TEXT_CHARS = 20  # below this, treat direct extraction as "no usable text"


def _validate_file(file_path: str, allowed_extensions: set[str]):
    path = Path(file_path)

    if not path.exists():
        return f"File not found: {file_path}"

    if path.suffix.lower() not in allowed_extensions:
        return f"Unsupported file extension: {path.suffix}"

    size = path.stat().st_size
    if size > MAX_FILE_SIZE_BYTES:
        return f"File too large ({size} bytes); limit is {MAX_FILE_SIZE_BYTES} bytes"

    return None


async def image_to_images(file_path: str):
    error = _validate_file(file_path, ALLOWED_IMAGE_EXTENSIONS)
    if error:
        logger.error("image_to_images validation failed: %s", error)
        return {"success": False, "error": error}

    return {"success": True, "data": [file_path]}


def extract_pdf_text_directly(file_path: str):
    """Pull selectable text straight out of the PDF (no OCR) via PyMuPDF."""
    error = _validate_file(file_path, ALLOWED_PDF_EXTENSIONS)
    if error:
        logger.error("extract_pdf_text_directly validation failed: %s", error)
        return {"success": False, "error": error}

    try:
        with fitz.open(file_path) as doc:
            total_pages = doc.page_count
            pages_to_read = min(total_pages, MAX_PDF_PAGES)
            texts = [doc.load_page(i).get_text() for i in range(pages_to_read)]

        text = "\n".join(t.strip() for t in texts if t.strip())
        pages_skipped = max(0, total_pages - pages_to_read)

        if pages_skipped:
            logger.warning(
                "Direct text extraction only read %d/%d page(s) of %s (page limit is %d)",
                pages_to_read, total_pages, file_path, MAX_PDF_PAGES,
            )

        logger.info("Direct PDF text extraction pulled %d char(s) from %s", len(text), file_path)

        return {
            "success": True,
            "data": {
                "text": text,
                "pages_processed": pages_to_read,
                "pages_skipped": pages_skipped,
            },
        }

    except Exception as exc:
        logger.exception("Direct PDF text extraction failed: %s", file_path)
        return {"success": False, "error": f"Direct PDF text extraction failed: {exc}"}


async def convert_pdf_to_images(file_path: str):
    error = _validate_file(file_path, ALLOWED_PDF_EXTENSIONS)
    if error:
        logger.error("convert_pdf_to_images validation failed: %s", error)
        return {"success": False, "error": error}

    try:
        IMAGE_DIR.mkdir(exist_ok=True)

        pdf_path = Path(file_path)

        with fitz.open(file_path) as doc:
            total_pages = doc.page_count

        pages_to_convert = min(total_pages, MAX_PDF_PAGES)
        pages_skipped = max(0, total_pages - pages_to_convert)

        images = convert_from_path(str(pdf_path), first_page=1, last_page=pages_to_convert)

        image_paths = []

        for index, image in enumerate(images):
            output_path = IMAGE_DIR / f"{pdf_path.stem}_page_{index+1}.png"
            image.save(output_path, "PNG")
            image_paths.append(str(output_path))

        if pages_skipped:
            logger.warning(
                "Skipped %d page(s) of %s (page limit is %d)",
                pages_skipped, file_path, MAX_PDF_PAGES,
            )

        logger.info("Converted %s into %d page image(s)", file_path, len(image_paths))

        return {
            "success": True,
            "data": {
                "image_paths": image_paths,
                "pages_processed": pages_to_convert,
                "pages_skipped": pages_skipped,
            },
        }

    except Exception as exc:
        logger.exception("Failed to convert PDF to images: %s", file_path)
        return {"success": False, "error": f"Failed to convert PDF to images: {exc}"}
