from fastapi import FastAPI
from api.schemas.request_response import (
    QARequest,
    QAResponse,
    RiskRequest,
    RiskResponse,
    SummaryRequest,
    SummaryResponse,
)

app = FastAPI(title="SamvidAI", version="0.1.0")

@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.post("/qa", response_model=QAResponse)
def legal_qa(payload: QARequest):
    answer = agent.answer_question(payload.question, payload.context)
    return {"answer": answer}


@app.post("/risk", response_model=RiskResponse)
def risk_analysis(payload: RiskRequest):
    result = agent.analyze_risk(payload.clause_text)
    return {"risk_analysis": result}


@app.post("/summarize", response_model=SummaryResponse)
def summarize(payload: SummaryRequest):
    summary = agent.summarize_document(payload.context)
    return {"summary": summary}
