from dataclasses import dataclass
from typing import List

from domain.enums import RiskLevel


@dataclass(frozen=True)
class Risk:
    """
    Represents risk detected in a clause.
    """
    clause_id: str
    categories: List[str]
    level: RiskLevel
    score: int
    explanation: str | None = None
