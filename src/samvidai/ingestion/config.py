from pathlib import Path
from enum import Enum


class DataSource(str, Enum):
    ACTS_AND_RULES = "acts_and_rules"
    GOVT_CONTRACTS = "govt_contracts"
    PUBLIC_JUDGMENTS = "public_judgments"
    SYNTHETIC_CONTRACTS = "synthetic_contracts"


DATA_ROOT = Path("data")
PROCESSED_ROOT = DATA_ROOT / "processed"


def get_source_path(source: DataSource) -> Path:
    return DATA_ROOT / source.value


def get_processed_path(source: DataSource) -> Path:
    return PROCESSED_ROOT / source.value
