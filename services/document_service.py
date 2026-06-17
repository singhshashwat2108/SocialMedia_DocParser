from fastapi import UploadFile
from services.converter_service import detect_document_type, image_to_images,convert_pdf_to_images
from services.ocr_service import extract_layout, extract_layout_from_images
from models.documents_type import DocumentType
import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploaded_files")


async def save_file(file: UploadFile):
    UPLOAD_DIR.mkdir(exist_ok=True)

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_name

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)

async def process_document(file: UploadFile):

    allowed_types = [
        "application/pdf",
        "image/png",
        "image/jpeg"
    ]

    if file.content_type not in allowed_types:
        return {
            "error": "Unsupported file type"
        }
    saved_path= await save_file(file)                              #SAVE THE DOC AND RETURN SAVED ADDRESS

    document_type = await detect_document_type(saved_path)         #DETECT DOCUMENT TYPE

    if document_type == DocumentType.PDF:
        image_paths = await convert_pdf_to_images(saved_path)       #PDF TO IMAGE CONVERSION

    elif document_type == DocumentType.IMAGE:
        image_paths = await image_to_images(saved_path)              #IMAGE IS AS IMAGE
         

    #text= extract_text(image_paths)                                #EXTRACT TEXT FROM THE SINGLE IMAGE


    # layout = extract_layout_from_images(image_paths)

    # return {
    #     "layout": layout
    # }
    layout = extract_layout_from_images(image_paths)       #STORES A LIST OF RETURNED TEXTS, FOR A LIST OF IMAGE_PATHS

    return {
        "filename":file.filename,
        "file_type": document_type,
        "Image_path": image_paths,
        "Text": text
    }