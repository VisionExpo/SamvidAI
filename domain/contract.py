from dataclasses import dataclass, field
from typing import List

from domain.clause import Clause
from domain.risk import Risk


@dataclass
class Contract:
    """
    Aggregate root for a legal contract.
    """
    contract_id: str
    clauses: List[Clause] = field(default_factory=list)
    risks: List[Risk] = field(default_factory=list)

    def add_clause(self, clause: Clause):
        self.clauses.append(clause)

    def add_risk(self, risk: Risk):
        self.risks.append(risk)

    def get_high_risks(self) -> List[Risk]:
        return [r for r in self.risks if r.level.value == "high"]
