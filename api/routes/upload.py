from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import fitz  # PyMuPDF

from samvidai.ingestion.config import DataSource, get_processed_path
from samvidai.layout.text_extractor import DigitalPDFTextExtractor
from samvidai.chunking.chunker import TextChunker
from samvidai.retrieval.embedding import EmbeddingModel
from samvidai.retrieval.index import VectorIndex
from samvidai.ingestion import pdf_to_images
from samvidai.layout.layoutlm import segment_layout

router = APIRouter()


def extract_text_from_pdf(pdf_path: Path) -> tuple:
    """
    Try to extract text from PDF. Returns pages with text.
    Falls back to OCR for scanned PDFs.
    """
    # First try direct text extraction
    doc = fitz.open(pdf_path)
    pages = []
    has_text = False
    
    for page_index, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            has_text = True
        pages.append({
            "page_number": page_index + 1,
            "text": text,
        })
    
    if has_text:
        return pages, "digital"
    
    # Try OCR for scanned PDFs
    try:
        # Convert PDF to images
        work_dir = pdf_path.parent / "temp_images"
        image_paths = pdf_to_images(str(pdf_path), str(work_dir))
        
        # Extract text using layout segmentation
        blocks = segment_layout(image_paths)
        
        # Convert blocks to pages format
        ocr_pages = []
        for i, page in enumerate(pages):
            page_blocks = [b for b in blocks if b.get("source_image", "").endswith(f"page_{i+1}.png")]
            combined_text = "\n".join([b.get("text", "") for b in page_blocks])
            ocr_pages.append({
                "page_number": page["page_number"],
                "text": combined_text,
            })
        
        # Cleanup temp images
        for img_path in image_paths:
            Path(img_path).unlink(missing_ok=True)
        work_dir.rmdir(missing_ok=True)
        
        if any(p["text"] for p in ocr_pages):
            return ocr_pages, "ocr"
    except Exception as e:
        print(f"OCR fallback failed: {e}")
    
    return pages, "empty"


def ingest_pdf(pdf_path: Path, source: DataSource):
    """
    Ingest a PDF and create its vector index.
    """
    processed_dir = get_processed_path(source)
    index_dir = processed_dir / "index"
    index_dir.mkdir(parents=True, exist_ok=True)

    # Extract text (with OCR fallback)
    pages, extraction_method = extract_text_from_pdf(pdf_path)

    # Chunk pages
    chunker = TextChunker(chunk_size=800, overlap=100)
    chunks = chunker.chunk_pages(
        pages=pages,
        metadata={
            "source": source.value,
            "document": pdf_path.name,
            "extraction_method": extraction_method,
        },
    )

    if not chunks:
        raise ValueError("No chunks created - PDF may be empty or extraction failed")

    # Build vector index
    embedder = EmbeddingModel()
    VectorIndex.build(
        chunks=chunks,
        embedder=embedder,
        output_dir=index_dir,
    )

    return len(chunks)


@router.post("/upload")
def upload_contract(
    file: UploadFile = File(...),
    data_source: str = "govt_contracts",
    auto_ingest: bool = True,
):
    dest = Path("data") / data_source / file.filename
    dest.parent.mkdir(parents=True, exist_ok=True)

    with open(dest, "wb") as f:
        f.write(file.file.read())

    # Auto-ingest the PDF if requested
    chunks_count = 0
    if auto_ingest:
        try:
            source = DataSource(data_source)
            chunks_count = ingest_pdf(dest, source)
        except Exception as e:
            return {
                "status": "uploaded",
                "filename": file.filename,
                "data_source": data_source,
                "pdf_path": str(dest),
                "ingestion_status": "failed",
                "ingestion_error": str(e),
            }

    return {
        "status": "uploaded",
        "filename": file.filename,
        "data_source": data_source,
        "pdf_path": str(dest),
        "ingestion_status": "success" if chunks_count > 0 else "skipped",
        "chunks_created": chunks_count,
    }
