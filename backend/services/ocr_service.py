import easyocr
from pydantic import BaseModel

reader = easyocr.Reader(['en'])


class OCRWord(BaseModel):
    text: str
    bbox: list[list[float]]
    confidence: float


def extract_layout(image_path: str):

    result = reader.readtext(image_path)

    words = []

    for bbox, text, confidence in result:

        words.append(
            OCRWord(
                text=text,
                bbox=bbox,
                confidence=float(confidence)
            )
        )

    return words


def extract_layout_from_images(image_paths: list[str]):
    return [extract_layout(image_path) for image_path in image_paths]
