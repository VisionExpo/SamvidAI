from pydantic import BaseModel
from typing import List


class ClauseCitation(BaseModel):
    clause_id: str
    text: str


class AnalyzeContractResponse(BaseModel):
    answer: str
    retrieved_clauses: List[ClauseCitation]
