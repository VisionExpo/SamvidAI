from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzeContractRequest(BaseModel):
    pdf_path: str = Field(min_length=1, max_length=500)
    question: str = Field(min_length=2, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=50)
    index_id: Optional[str] = Field(
        default=None,
        pattern=r"^(acts_and_rules|govt_contracts|public_judgments|synthetic_contracts):[a-f0-9]{32}$",
    )


class ClauseCitation(BaseModel):
    clause_id: str
    text: str


class AnalyzeContractResponse(BaseModel):
    answer: str
    retrieved_clauses: List[ClauseCitation]
