from .pdf_to_image import pdf_to_images
from .preprocess import preprocess_image

def ingest_pdf(pdf_path: str, work_dir: str):
    image_paths = pdf_to_images(pdf_path, work_dir)
    processed = [preprocess_image(p) for p in image_paths]
    return processed
