import easyocr

from models.ocr_word import OCRWord

reader = easyocr.Reader(['en'])

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