from fastapi import APIRouter, UploadFile, File

from services.pdf_service import image_to_images, convert_pdf_to_images
from services.ocr_service import extract_layout_from_images
from utils.file_helpers import DocumentType, detect_document_type, save_file

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


async def process_document(file: UploadFile):

    allowed_types = [
        "application/pdf",
        "image/png",
        "image/jpeg"
    ]

    if file.content_type not in allowed_types:
        return {"success": False, "error": "Unsupported file type"}

    saved_path = await save_file(file)                              #SAVE THE DOC AND RETURN SAVED ADDRESS

    document_type = await detect_document_type(saved_path)          #DETECT DOCUMENT TYPE

    if document_type == DocumentType.PDF:
        conversion = await convert_pdf_to_images(saved_path)        #PDF TO IMAGE CONVERSION

    elif document_type == DocumentType.IMAGE:
        conversion = await image_to_images(saved_path)               #IMAGE IS AS IMAGE

    else:
        return {"success": False, "error": f"Unsupported document type: {document_type}"}

    if not conversion["success"]:
        return conversion

    image_paths = conversion["data"]

    layout_result = extract_layout_from_images(image_paths)        #STORES A LIST OF RETURNED TEXTS, FOR A LIST OF IMAGE_PATHS

    if not layout_result["success"]:
        return layout_result

    return {
        "success": True,
        "data": {
            "filename": file.filename,
            "file_type": document_type,
            "image_paths": image_paths,
            "layout": layout_result["data"],
        },
    }


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)):
    return await process_document(file)
