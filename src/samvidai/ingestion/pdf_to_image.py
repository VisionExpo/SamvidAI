import os
from pathlib import Path
import fitz  # PyMuPDF
from pdf2image import convert_from_path


def _render_with_pymupdf(pdf_path: str, output_dir: Path) -> list[str]:
    """
    Poppler-free fallback: render pages directly with PyMuPDF.
    """
    image_paths = []
    zoom = 300 / 72  # match ~300 DPI output from pdf2image
    matrix = fitz.Matrix(zoom, zoom)

    doc = fitz.open(pdf_path)
    try:
        for i, page in enumerate(doc):
            path = output_dir / f"page_{i+1}.png"
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            pix.save(path)
            image_paths.append(str(path))
    finally:
        doc.close()

    return image_paths

def pdf_to_images(pdf_path: str, output_dir: str) -> list[str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    poppler_path = os.getenv("POPPLER_PATH") or None
    try:
        images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        image_paths = []
        for i, img in enumerate(images):
            path = output_dir / f"page_{i+1}.png"
            img.save(path, "PNG")
            image_paths.append(str(path))
        return image_paths
    except Exception:
        return _render_with_pymupdf(pdf_path, output_dir)
