from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.pdf_service import image_to_images, convert_pdf_to_images
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


async def process_document(file: UploadFile):

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    saved_path = await save_file(file)                              #SAVE THE DOC AND RETURN SAVED ADDRESS

    document_type = await detect_document_type(saved_path)          #DETECT DOCUMENT TYPE

    if document_type == DocumentType.PDF:
        conversion = await convert_pdf_to_images(saved_path)        #PDF TO IMAGE CONVERSION

    elif document_type == DocumentType.IMAGE:
        conversion = await image_to_images(saved_path)               #IMAGE IS AS IMAGE

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported document type: {document_type}")

    if not conversion["success"]:
        raise HTTPException(status_code=400, detail=conversion["error"])

    image_paths = conversion["data"]

    layout_result = extract_layout_from_images(image_paths)        #STORES A LIST OF RETURNED TEXTS, FOR A LIST OF IMAGE_PATHS

    if not layout_result["success"]:
        raise HTTPException(status_code=500, detail=layout_result["error"])

    pages = layout_result["data"]
    text = "\n".join(word.text for page in pages for word in page)

    return {"text": text}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)):
    return await process_document(file)
