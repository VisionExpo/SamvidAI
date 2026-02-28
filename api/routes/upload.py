from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import tempfile
from uuid import uuid4
import fitz  # PyMuPDF

from samvidai.ingestion.config import DataSource, get_processed_path
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
        # Python <3.12 compatibility: Path.rmdir has no missing_ok parameter.
        shutil.rmtree(work_dir, ignore_errors=True)
        
        if any(p["text"] for p in ocr_pages):
            return ocr_pages, "ocr"
    except Exception as e:
        print(f"OCR fallback failed: {e}")
    
    return pages, "empty"


def ingest_pdf(
    pdf_path: Path,
    source: DataSource,
    index_dir: Path | None = None,
    document_name: str | None = None,
):
    """
    Ingest a PDF and create its vector index.
    """
    if index_dir is None:
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
            "document": document_name or pdf_path.name,
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
    data_source: DataSource = DataSource.GOVT_CONTRACTS,
    auto_ingest: bool = True,
):
    source = data_source
    filename = Path(file.filename or "uploaded.pdf").name
    upload_id = uuid4().hex
    upload_index_dir = get_processed_path(source) / "uploads" / upload_id

    temp_pdf_path = None
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        tmp.write(file.file.read())
        tmp.flush()
        temp_pdf_path = Path(tmp.name)
    finally:
        tmp.close()

    # Auto-ingest the PDF if requested
    chunks_count = 0
    index_id = None
    if auto_ingest:
        index_id = f"{source.value}:{upload_id}"
        try:
            chunks_count = ingest_pdf(
                temp_pdf_path,
                source,
                index_dir=upload_index_dir,
                document_name=filename,
            )
        except Exception as e:
            return {
                "status": "uploaded",
                "filename": filename,
                "data_source": source.value,
                "pdf_path": f"virtual://{source.value}/{filename}",
                "index_id": index_id,
                "ingestion_status": "failed",
                "ingestion_error": str(e),
            }
        finally:
            if temp_pdf_path is not None:
                temp_pdf_path.unlink(missing_ok=True)
    else:
        if temp_pdf_path is not None:
            temp_pdf_path.unlink(missing_ok=True)

    return {
        "status": "uploaded",
        "filename": filename,
        "data_source": source.value,
        "pdf_path": f"virtual://{source.value}/{filename}",
        "index_id": index_id,
        "ingestion_status": "success" if chunks_count > 0 else "skipped",
        "chunks_created": chunks_count,
    }
