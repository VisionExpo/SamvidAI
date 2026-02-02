from fastapi import APIRouter, Depends

from api.deps import get_retriever, get_legal_agent
from api.schemas.rag import (
    AnalyzeContractRequest,
    AnalyzeContractResponse,
)
from api.schemas.risk import (
    AnalyzeRiskRequest,
    AnalyzeRiskResponse,
)

from samvidai.ingestion import ingest_pdf
from samvidai.layout import segment_layout
from samvidai.retrieval import Retriever
from samvidai.llm.agents import LegalAgent
from samvidai.risk_engine import classify_clause, score_risks


router = APIRouter(tags=["Analysis"])


@router.post(
    "/analyze-contract",
    response_model=AnalyzeContractResponse,
)
def analyze_contract(
    payload: AnalyzeContractRequest,
    retriever: Retriever = Depends(get_retriever),
    agent: LegalAgent = Depends(get_legal_agent),
):
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

    return {
        "answer": answer,
        "retrieved_clauses": [
            {"clause_id": c["clause_id"], "text": c["text"]}
            for c in retrieved
        ],
    }


@router.post(
    "/analyze-risk",
    response_model=AnalyzeRiskResponse,
)
def analyze_risk(
    payload: AnalyzeRiskRequest,
    retriever: Retriever = Depends(get_retriever),
):
    images = ingest_pdf(
        pdf_path=payload.pdf_path,
        work_dir="data/processed"
    )

    blocks = segment_layout(images)
    retriever.index(blocks)

    retrieved = retriever.retrieve(payload.question)

    risks = []
    for clause in retrieved:
        detected = classify_clause(clause["text"])
        risks.append({
            "clause_id": clause["clause_id"],
            "risks": detected,
            "risk_score": score_risks(detected),
        })

    return {"risks": risks}
