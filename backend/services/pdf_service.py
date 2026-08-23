import logging
from pathlib import Path

from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

IMAGE_DIR = Path("converted_images")
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}


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


async def convert_pdf_to_images(file_path: str):
    error = _validate_file(file_path, ALLOWED_PDF_EXTENSIONS)
    if error:
        logger.error("convert_pdf_to_images validation failed: %s", error)
        return {"success": False, "error": error}

    try:
        IMAGE_DIR.mkdir(exist_ok=True)

        pdf_path = Path(file_path)
        images = convert_from_path(str(pdf_path))

        image_paths = []

        for index, image in enumerate(images):
            output_path = IMAGE_DIR / f"{pdf_path.stem}_page_{index+1}.png"
            image.save(output_path, "PNG")
            image_paths.append(str(output_path))

        logger.info("Converted %s into %d page image(s)", file_path, len(image_paths))
        return {"success": True, "data": image_paths}

    except Exception as exc:
        logger.exception("Failed to convert PDF to images: %s", file_path)
        return {"success": False, "error": f"Failed to convert PDF to images: {exc}"}
