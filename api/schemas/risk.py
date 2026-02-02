from pydantic import BaseModel
from typing import List


class ClauseRisk(BaseModel):
    clause_id: str
    risks: List[str]
    risk_score: int


class AnalyzeRiskRequest(BaseModel):
    pdf_path: str
    question: str


class AnalyzeRiskResponse(BaseModel):
    risks: List[ClauseRisk]
