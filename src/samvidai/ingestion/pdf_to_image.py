from pdf2image import convert_from_path
from pathlib import Path

def pdf_to_images(pdf_path: str, output_dir: str) -> list[str]:
    """
    Convert PDF pages to images
    Returns list of image paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exits_ok=True)

    images = convert_from_path(pdf_path, dpi=300)
    image_paths = []

    for i, image in enumerate(images):
        img_path = output_dir f"page_{i+1}.png"
        image.save(img_path, "PNG")
        image_paths.append(str(img_path))
