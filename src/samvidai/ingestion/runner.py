import json
from pathlib import Path

from samvidai.layout.text_extractor import DigitalPDFTextExtractor
from samvidai.ingestion.config import DataSource, get_source_path, get_processed_path


def ingest_source(source: DataSource) -> None:
    source_dir = get_source_path(source)
    out_dir = get_processed_path(source)
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(source_dir.glob("*.pdf"))

    if not pdf_files:
        raise RuntimeError(f"No PDFs found in {source_dir}")

    for pdf_path in pdf_files:
        extractor = DigitalPDFTextExtractor(pdf_path)
        pages = extractor.extract()

        out_file = out_dir / f"{pdf_path.stem}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "source": source.value,
                    "document_name": pdf_path.name,
                    "pages": pages,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"[INGESTED] {pdf_path.name} → {out_file}")
