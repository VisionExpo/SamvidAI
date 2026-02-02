from fastapi import FastAPI

from api.schemas.request_response import (
    HealthResponse,
    QARequest,
    QAResponse,
    RiskRequest,
    RiskResponse,
    SummaryRequest,
    SummaryResponse,
)

from api.schemas.rag import (
    AnalyzeContractRequest,
    AnalyzeContractResponse,
)

from api.schemas.risk import (
    AnalyzeRiskRequest,
    AnalyzeRiskResponse,
)

from samvidai.risk_engine import classify_clause, score_risks
from samvidai.ingestion import ingest_pdf
from samvidai.layout import segment_layout
from samvidai.retrieval import Retriever
from samvidai.llm.agents import LegalAgent


app = FastAPI(title="SamvidAI", version="0.1.0")
agent = LegalAgent()


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


@app.post(
    "/analyze-contract",
    response_model=AnalyzeContractResponse,
)
def analyze_contract(payload: AnalyzeContractRequest):

    retriever = Retriever()

    images = ingest_pdf(
        pdf_path=payload.pdf_path,
        work_dir="data/processed"
    )

    blocks = segment_layout(images)
    retriever.index(blocks)

    retrieved = retriever.retrieve(payload.question)
    context = [c["text"] for c in retrieved]

    answer = agent.answer_question(
        question=payload.question,
        context=context
    )

    if answer == "Not found in the provided contract.":
        return {"answer": answer, "retrieved_clauses": []}

    citations = [
        {"clause_id": c["clause_id"], "text": c["text"]}
        for c in retrieved
    ]

    return {
        "answer": answer,
        "retrieved_clauses": citations,
    }

@app.post(
    "/analyze-risk",
    response_model=AnalyzeRiskResponse,
)
def analyze_risk(payload: AnalyzeRiskRequest):

    retriever = Retriever()

    images = ingest_pdf(
        pdf_path=payload.pdf_path,
        work_dir="data/processed"
    )

    blocks = segment_layout(images)
    retriever.index(blocks)

    retrieved = retriever.retrieve(payload.question)

    risk_results = []

    for clause in retrieved:
        risks = classify_clause(clause["text"])
        score = score_risks(risks)

        risk_results.append({
            "clause_id": clause["clause_id"],
            "risks": risks,
            "risk_score": score,
        })

    return {"risks": risk_results}
