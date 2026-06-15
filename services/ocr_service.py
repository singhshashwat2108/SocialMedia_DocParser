import keras_ocr

from models.ocr_word import OCRWord 

pipeline = keras_ocr.pipeline.Pipeline()

def extract_layout(
    image_path: str
):

    image = keras_ocr.tools.read(image_path)

    predictions = pipeline.recognize(
        [image]
    )[0]

    words = []

    for text, box in predictions:

        words.append(
            OCRWord(
                text=text,
                bbox=box.tolist()
            )
        )

    return words


def extract_layout_from_images(
    image_paths: list[str]
):

    pages = []

    for image_path in image_paths:

        page_words = extract_layout(
            image_path
        )

        pages.append(
            {
                "image": image_path,
                "words": page_words
            }
        )

    return pages