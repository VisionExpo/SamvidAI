from dataclasses import dataclass
from typing import Optional

from domain.enums import ClauseType


@dataclass(frozen=True)
class Clause:
    """
    Represents a single contract clause.
    """
    clause_id: str
    text: str
    clause_type: ClauseType = ClauseType.OTHER
    source_page: Optional[int] = None
