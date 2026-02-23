from pydantic import BaseModel
from typing import List


class ClauseRisk(BaseModel):
    """Schema for individual clause risk analysis."""
    clause_id: str
    text: str
    risk_level: str
    reason: str


class AnalyzeRiskRequest(BaseModel):
    """Request schema for risk analysis endpoint."""
    pdf_path: str
    top_k: int = 10


class AnalyzeRiskResponse(BaseModel):
    """Response schema for risk analysis endpoint matching v1.0 roadmap."""
    risk_score: int
    risk_level: str
    clauses_analyzed: int
    clauses: List[ClauseRisk]
