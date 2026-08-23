from enum import Enum
from pathlib import Path
import uuid

from fastapi import UploadFile

UPLOAD_DIR = Path("uploaded_files")


class DocumentType(str, Enum):
    PDF = "pdf"
    IMAGE = "image"
    DOCX = "docx"
    PPTX = "pptx"
    TXT = "txt"
    UNSUPPORTED = "unsupported"


async def detect_document_type(
    file_path: str
):
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return DocumentType.PDF

    elif suffix == ".docx":
        return DocumentType.DOCX

    elif suffix == ".pptx":
        return DocumentType.PPTX

    elif suffix == ".txt":
        return DocumentType.TXT

    elif suffix in [".png", ".jpg", ".jpeg", ".webp"]:
        return DocumentType.IMAGE

    return DocumentType.UNSUPPORTED


async def save_file(file: UploadFile):
    UPLOAD_DIR.mkdir(exist_ok=True)

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_name

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)
