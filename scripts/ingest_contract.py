import sys
from pathlib import Path

from samvidai.ingestion.config import DataSource, get_processed_path
from samvidai.layout.text_extractor import DigitalPDFTextExtractor
from samvidai.chunking.chunker import TextChunker
from samvidai.retrieval.embedding import EmbeddingModel
from samvidai.retrieval.index import VectorIndex


def main(pdf_path: Path):
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # 1️⃣ Resolve data source dynamically
    source = DataSource.from_pdf_path(pdf_path)
    processed_dir = get_processed_path(source)
    index_dir = processed_dir / "index"
    index_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Ingesting {pdf_path}")
    print(f"[INFO] Data source: {source.value}")

    # 2️⃣ Extract text
    extractor = DigitalPDFTextExtractor(pdf_path)
    pages = extractor.extract()
    print(f"[INFO] Extracted {len(pages)} pages")

    # 3️⃣ Chunk pages
    chunker = TextChunker(chunk_size=800, overlap=100)
    chunks = chunker.chunk_pages(
        pages=pages,
        metadata={
            "source": source.value,
            "document": pdf_path.name,
        },
    )
    print(f"[INFO] Created {len(chunks)} chunks")

    # 4️⃣ Build vector index
    embedder = EmbeddingModel()
    VectorIndex.build(
        chunks=chunks,
        embedder=embedder,
        output_dir=index_dir,
    )

    print(f"[SUCCESS] Built index at {index_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/ingest_contract.py <pdf_path>")
        sys.exit(1)

    main(Path(sys.argv[1]))
