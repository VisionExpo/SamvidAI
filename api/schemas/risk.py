from pydantic import BaseModel
from typing import List
from typing import Optional


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
    index_id: Optional[str] = None


class AnalyzeRiskResponse(BaseModel):
    """Response schema for risk analysis endpoint matching v1.0 roadmap."""
    risk_score: int
    risk_level: str
    clauses_analyzed: int
    clauses: List[ClauseRisk]
