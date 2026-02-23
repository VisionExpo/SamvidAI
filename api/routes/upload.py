from fastapi import APIRouter, UploadFile, File
from pathlib import Path

from samvidai.ingestion.config import DataSource, get_processed_path
from samvidai.layout.text_extractor import DigitalPDFTextExtractor
from samvidai.chunking.chunker import TextChunker
from samvidai.retrieval.embedding import EmbeddingModel
from samvidai.retrieval.index import VectorIndex

router = APIRouter()


def ingest_pdf(pdf_path: Path, source: DataSource):
    """
    Ingest a PDF and create its vector index.
    """
    processed_dir = get_processed_path(source)
    index_dir = processed_dir / "index"
    index_dir.mkdir(parents=True, exist_ok=True)

    # Extract text
    extractor = DigitalPDFTextExtractor(pdf_path)
    pages = extractor.extract()

    # Chunk pages
    chunker = TextChunker(chunk_size=800, overlap=100)
    chunks = chunker.chunk_pages(
        pages=pages,
        metadata={
            "source": source.value,
            "document": pdf_path.name,
        },
    )

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
                "ingestion_status": "failed",
                "ingestion_error": str(e),
            }

    return {
        "status": "uploaded",
        "filename": file.filename,
        "data_source": data_source,
        "ingestion_status": "success" if chunks_count > 0 else "skipped",
        "chunks_created": chunks_count,
    }
