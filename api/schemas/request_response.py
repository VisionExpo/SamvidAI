from pydantic import BaseModel, Field
from typing import List, Optional


# -------------------------
# Health
# -------------------------

class HealthResponse(BaseModel):
    status: str = "ok"


# -------------------------
# Question Answering
# -------------------------

class QARequest(BaseModel):
    question: str = Field(..., description="Legal question asked by the user")
    context: List[str] = Field(
        ..., description="Relevant contract clauses or chunks"
    )


class QAResponse(BaseModel):
    answer: str = Field(..., description="Answer generated from contract context")


# -------------------------
# Risk Analysis
# -------------------------

class RiskRequest(BaseModel):
    clause_text: str = Field(..., description="Single contract clause")


class RiskResponse(BaseModel):
    risk_analysis: str = Field(
        ..., description="Risk level and legal explanation"
    )


# -------------------------
# Summarization
# -------------------------

class SummaryRequest(BaseModel):
    context: List[str] = Field(
        ..., description="Contract text or clauses to summarize"
    )


class SummaryResponse(BaseModel):
    summary: str = Field(..., description="Legally accurate summary")