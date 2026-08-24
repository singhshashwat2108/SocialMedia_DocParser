import asyncio

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.pdf_service import (
    image_to_images,
    convert_pdf_to_images,
    extract_pdf_text_directly,
    MIN_DIRECT_TEXT_CHARS,
)
from backend.services.ocr_service import extract_layout_from_images
from backend.utils.file_helpers import DocumentType, detect_document_type, save_file

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/webp",
}

UPLOAD_PIPELINE_TIMEOUT_SECONDS = 45


def _ocr_images_to_text(image_paths):
    layout_result = extract_layout_from_images(image_paths)

    if not layout_result["success"]:
        raise HTTPException(status_code=500, detail=layout_result["error"])

    text = layout_result["data"]["text"]
    return text, layout_result.get("truncated", False)


async def process_document(file: UploadFile):

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    saved_path = await save_file(file)                              #SAVE THE DOC AND RETURN SAVED ADDRESS

    document_type = await detect_document_type(saved_path)          #DETECT DOCUMENT TYPE

    if document_type == DocumentType.PDF:

        direct = extract_pdf_text_directly(saved_path)              #TRY SELECTABLE TEXT FIRST (NO OCR)

        if direct["success"] and len(direct["data"]["text"]) >= MIN_DIRECT_TEXT_CHARS:
            response = {"text": direct["data"]["text"]}
            if direct["data"]["pages_skipped"]:
                response["pages_processed"] = direct["data"]["pages_processed"]
                response["pages_skipped"] = direct["data"]["pages_skipped"]
            return response

        conversion = await convert_pdf_to_images(saved_path)        #FALL BACK TO OCR ON PAGE IMAGES

        if not conversion["success"]:
            raise HTTPException(status_code=400, detail=conversion["error"])

        image_paths = conversion["data"]["image_paths"]
        text, truncated = _ocr_images_to_text(image_paths)

        response = {"text": text}
        if conversion["data"]["pages_skipped"]:
            response["pages_processed"] = conversion["data"]["pages_processed"]
            response["pages_skipped"] = conversion["data"]["pages_skipped"]
        if truncated:
            response["truncated"] = True

        return response

    elif document_type == DocumentType.IMAGE:
        conversion = await image_to_images(saved_path)               #IMAGE IS AS IMAGE

        if not conversion["success"]:
            raise HTTPException(status_code=400, detail=conversion["error"])

        image_paths = conversion["data"]
        text, truncated = _ocr_images_to_text(image_paths)

        response = {"text": text}
        if truncated:
            response["truncated"] = True

        return response

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported document type: {document_type}")


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        return await asyncio.wait_for(process_document(file), timeout=UPLOAD_PIPELINE_TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail=(
                f"Processing this document took longer than {UPLOAD_PIPELINE_TIMEOUT_SECONDS}s. "
                "Try a smaller file or fewer pages."
            ),
        )
