from pathlib import Path
from enum import Enum


class DataSource(str, Enum):
    ACTS_AND_RULES = "acts_and_rules"
    GOVT_CONTRACTS = "govt_contracts"
    PUBLIC_JUDGMENTS = "public_judgments"
    SYNTHETIC_CONTRACTS = "synthetic_contracts"

    @classmethod
    def from_pdf_path(cls, pdf_path: Path) -> "DataSource":
        path = str(pdf_path).lower()

        if "acts_and_rules" in path:
            return cls.ACTS_AND_RULES
        if "govt_contracts" in path:
            return cls.GOVT_CONTRACTS
        if "public_judgments" in path:
            return cls.PUBLIC_JUDGMENTS
        if "synthetic_contracts" in path:
            return cls.SYNTHETIC_CONTRACTS

        raise ValueError(
            f"Cannot infer DataSource from path: {pdf_path}"
        )


DATA_ROOT = Path("data")
PROCESSED_ROOT = DATA_ROOT / "processed"


def get_source_path(source: DataSource) -> Path:
    return DATA_ROOT / source.value


def get_processed_path(source: DataSource) -> Path:
    return PROCESSED_ROOT / source.value
