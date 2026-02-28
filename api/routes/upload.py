import os
import re
import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

import fitz  # PyMuPDF
from fastapi import APIRouter, File, HTTPException, UploadFile

from api.schemas.upload import UploadIngestionResult, UploadResponse, UploadStorageInfo
from samvidai.chunking.chunker import TextChunker
from samvidai.ingestion import pdf_to_images
from samvidai.ingestion.config import DataSource, get_processed_path
from samvidai.layout.layoutlm import segment_layout
from samvidai.retrieval.embedding import EmbeddingModel
from samvidai.retrieval.index import VectorIndex

router = APIRouter()

MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", "26214400"))  # 25 MB default
VALID_CONTENT_TYPES = {"application/pdf", "application/x-pdf", "application/octet-stream"}
SAFE_FILENAME_RE = re.compile(r"^[A-Za-z0-9._ -]{1,180}$")


def _validate_pdf_upload(file: UploadFile) -> str:
    if not file.filename:
        raise HTTPException(status_code=400, detail="filename is required")

    filename = Path(file.filename).name.strip()
    if not filename:
        raise HTTPException(status_code=400, detail="filename is required")
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf uploads are supported")
    if not SAFE_FILENAME_RE.fullmatch(filename):
        raise HTTPException(status_code=400, detail="filename contains unsupported characters")

    content_type = (file.content_type or "").lower()
    if content_type not in VALID_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail=f"Unsupported content_type: {file.content_type}")

    return filename


def _store_upload_temporarily(file: UploadFile) -> tuple[Path, int]:
    size_bytes = 0
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_pdf_path = Path(tmp.name)

    try:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            size_bytes += len(chunk)
            if size_bytes > MAX_UPLOAD_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail=f"Uploaded file exceeds MAX_UPLOAD_BYTES={MAX_UPLOAD_BYTES}",
                )
            tmp.write(chunk)
        tmp.flush()
    except Exception:
        tmp.close()
        temp_pdf_path.unlink(missing_ok=True)
        raise
    finally:
        tmp.close()

    if size_bytes == 0:
        temp_pdf_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    return temp_pdf_path, size_bytes


def extract_text_from_pdf(pdf_path: Path) -> tuple:
    """
    Try to extract text from PDF. Returns pages with text.
    Falls back to OCR for scanned PDFs.
    """
    pages = []
    has_text = False

    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                has_text = True
            pages.append(
                {
                    "page_number": page_index + 1,
                    "text": text,
                }
            )

    if has_text:
        return pages, "digital"

    work_dir = Path(tempfile.mkdtemp(prefix="samvidai_ocr_"))
    image_paths = []
    try:
        image_paths = pdf_to_images(str(pdf_path), str(work_dir))
        blocks = segment_layout(image_paths)

        ocr_pages = []
        for i, page in enumerate(pages):
            page_blocks = [
                b for b in blocks if b.get("source_image", "").endswith(f"page_{i+1}.png")
            ]
            combined_text = "\n".join([b.get("text", "") for b in page_blocks])
            ocr_pages.append(
                {
                    "page_number": page["page_number"],
                    "text": combined_text,
                }
            )

        if any(p["text"] for p in ocr_pages):
            return ocr_pages, "ocr"
    except Exception as exc:
        print(f"OCR fallback failed: {exc}")
    finally:
        for img_path in image_paths:
            Path(img_path).unlink(missing_ok=True)
        shutil.rmtree(work_dir, ignore_errors=True)

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

    pages, extraction_method = extract_text_from_pdf(pdf_path)

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

    embedder = EmbeddingModel()
    VectorIndex.build(
        chunks=chunks,
        embedder=embedder,
        output_dir=index_dir,
    )

    return len(chunks)


@router.post("/upload", response_model=UploadResponse)
def upload_contract(
    file: UploadFile = File(...),
    data_source: DataSource = DataSource.GOVT_CONTRACTS,
    auto_ingest: bool = True,
):
    source = data_source
    filename = _validate_pdf_upload(file)

    upload_id = uuid4().hex
    index_id = f"{source.value}:{upload_id}" if auto_ingest else None
    upload_index_dir = get_processed_path(source) / "uploads" / upload_id

    temp_pdf_path, size_bytes = _store_upload_temporarily(file)

    chunks_count = 0
    ingestion_status = "skipped"
    ingestion_error = None

    try:
        if auto_ingest:
            chunks_count = ingest_pdf(
                temp_pdf_path,
                source,
                index_dir=upload_index_dir,
                document_name=filename,
            )
            ingestion_status = "success"
    except Exception as exc:
        ingestion_status = "failed"
        ingestion_error = str(exc)
    finally:
        temp_pdf_path.unlink(missing_ok=True)

    virtual_pdf_path = f"virtual://{source.value}/{filename}"

    return UploadResponse(
        status="uploaded",
        upload_id=upload_id,
        filename=filename,
        content_type=file.content_type or "application/pdf",
        size_bytes=size_bytes,
        data_source=source.value,
        index_id=index_id,
        pdf_path=virtual_pdf_path,
        ingestion_status=ingestion_status,
        ingestion_error=ingestion_error,
        chunks_created=chunks_count,
        ingestion=UploadIngestionResult(
            status=ingestion_status,
            chunks_created=chunks_count,
            error=ingestion_error,
        ),
        storage=UploadStorageInfo(
            persisted_pdf=False,
            pdf_virtual_path=virtual_pdf_path,
            index_dir=str(upload_index_dir) if auto_ingest else None,
        ),
    )
