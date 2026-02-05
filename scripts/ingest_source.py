import sys
from samvidai.ingestion.config import DataSource
from samvidai.ingestion.runner import ingest_source


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python scripts/ingest_source.py <data_source>\n"
            f"Options: {[s.value for s in DataSource]}"
        )

    source = DataSource(sys.argv[1])
    ingest_source(source)


if __name__ == "__main__":
    main()
