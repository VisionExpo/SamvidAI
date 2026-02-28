from pydantic import BaseModel, Field
from typing import List


class ClauseRisk(BaseModel):
    """Schema for individual clause risk analysis."""
    clause_id: str
    text: str
    risk_level: str
    reason: str


class AnalyzeRiskRequest(BaseModel):
    """Request schema for risk analysis endpoint."""
    index_id: str = Field(pattern=r"^(acts_and_rules|govt_contracts|public_judgments|synthetic_contracts):[a-f0-9]{32}$")
    top_k: int = Field(default=10, ge=1, le=50)


class AnalyzeRiskResponse(BaseModel):
    """Response schema for risk analysis endpoint matching v1.0 roadmap."""
    risk_score: int
    risk_level: str
    clauses_analyzed: int
    clauses: List[ClauseRisk]
