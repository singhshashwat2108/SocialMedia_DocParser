from pathlib import Path

from pdf2image import convert_from_path

IMAGE_DIR = Path("converted_images")


async def image_to_images(file_path: str):
    return [file_path]


async def convert_pdf_to_images(file_path: str):

    IMAGE_DIR.mkdir(
        exist_ok=True
    )

    pdf_path = Path(file_path)

    images = convert_from_path(str(pdf_path))

    image_paths = []

    for index, image in enumerate(images):

        output_path = (IMAGE_DIR / f"{pdf_path.stem}_page_{index+1}.png")

        image.save(output_path,"PNG")

        image_paths.append(str(output_path))

    return image_paths
