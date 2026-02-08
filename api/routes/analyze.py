from fastapi import APIRouter, Depends, HTTPException

from api.schemas.rag import (
    AnalyzeContractRequest,
    AnalyzeContractResponse,
)
from api.schemas.risk import (
    AnalyzeRiskRequest,
    AnalyzeRiskResponse,
)
from api.deps import get_embedder, get_legal_agent, get_risk_engine

from samvidai.retrieval.index import VectorIndex
from samvidai.ingestion.config import DataSource, get_processed_path

router = APIRouter()


@router.post("/analyze/qa", response_model=AnalyzeContractResponse)
def analyze_qa(
    req: AnalyzeContractRequest,
    embedder=Depends(get_embedder),
    agent=Depends(get_legal_agent),
):
    source = DataSource.from_pdf_path(req.pdf_path)
    index_dir = get_processed_path(source) / "index"

    index = VectorIndex.load(
        index_dir / "vectors.index",
        index_dir / "metadata.json",
    )

    query_embedding = embedder.encode([req.question])
    clauses = index.search(query_embedding, top_k=req.top_k)

    answer = agent.answer_question(
        req.question,
        clauses,
    )

    return AnalyzeContractResponse(
        answer=answer,
        retrieved_clauses=[
            {"clause_id": c["id"], "text": c["text"]}
            for c in clauses
        ],
    )


@router.post("/analyze/risk", response_model=AnalyzeRiskResponse)
def analyze_risk(
    req: AnalyzeRiskRequest,
    embedder=Depends(get_embedder),
    agent=Depends(get_legal_agent),
    engines=Depends(get_risk_engine),
):
    classifier, scorer = engines

    source = DataSource.from_pdf_path(req.pdf_path)
    index_dir = get_processed_path(source) / "index"

    index = VectorIndex.load(
        index_dir / "vectors.index",
        index_dir / "metadata.json",
    )

    query_embedding = embedder.encode(
        ["termination penalty liability indemnity arbitration breach"]
    )
    clauses = index.search(query_embedding, top_k=10)

    risks = []
    for clause in clauses:
        analysis = agent.analyze_clause_risk(clause["text"])
        risks.append(
            {
                "clause_id": clause["id"],
                "risks": [analysis],
                "risk_score": classifier.classify_clause(analysis),
            }
        )

    return AnalyzeRiskResponse(risks=risks)
