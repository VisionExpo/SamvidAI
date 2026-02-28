import re

from fastapi import APIRouter, Depends, HTTPException

from api.schemas.rag import (
    AnalyzeContractRequest,
    AnalyzeContractResponse,
)
from api.schemas.risk import (
    AnalyzeRiskRequest,
    AnalyzeRiskResponse,
    ClauseRisk,
)
from api.deps import get_embedder, get_legal_agent, get_risk_engine

from samvidai.retrieval.index import VectorIndex
from samvidai.ingestion.config import DataSource, get_processed_path

router = APIRouter()

# Centralized risk query as per roadmap
RISK_QUERY = """
termination indemnity liability penalty damages breach
arbitration governing law force majeure confidentiality
"""


def _format_llm_error(exc: Exception) -> str:
    msg = " ".join(str(exc).split())
    if len(msg) > 240:
        msg = msg[:237] + "..."
    return (
        f"LLM analysis unavailable ({exc.__class__.__name__}: {msg}). "
        "Applied rule-based risk classification from clause text."
    )


def _resolve_index_dir(pdf_path: str, index_id: str | None):
    if index_id:
        try:
            source_str, upload_id = index_id.split(":", 1)
            source = DataSource(source_str)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Invalid index_id format: {index_id}") from exc
        if not re.fullmatch(r"[a-f0-9]{32}", upload_id):
            raise HTTPException(status_code=400, detail=f"Invalid index_id format: {index_id}")

        index_dir = get_processed_path(source) / "uploads" / upload_id
        if not (index_dir / "vectors.index").exists() or not (index_dir / "metadata.json").exists():
            raise HTTPException(status_code=404, detail=f"Index not found for index_id: {index_id}")
        return index_dir

    source = DataSource.from_pdf_path(pdf_path)
    return get_processed_path(source) / "index"


def _resolve_uploaded_index_dir(index_id: str):
    try:
        source_str, upload_id = index_id.split(":", 1)
        source = DataSource(source_str)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid index_id format: {index_id}") from exc

    if not re.fullmatch(r"[a-f0-9]{32}", upload_id):
        raise HTTPException(status_code=400, detail=f"Invalid index_id format: {index_id}")

    index_dir = get_processed_path(source) / "uploads" / upload_id
    if not (index_dir / "vectors.index").exists() or not (index_dir / "metadata.json").exists():
        raise HTTPException(status_code=404, detail=f"Index not found for index_id: {index_id}")
    return index_dir


@router.post("/qa", response_model=AnalyzeContractResponse)
def analyze_qa(
    req: AnalyzeContractRequest,
    embedder=Depends(get_embedder),
    agent=Depends(get_legal_agent),
):
    index_dir = _resolve_index_dir(req.pdf_path, req.index_id)

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
            {
                "clause_id": f"page_{c['page_number']}_chunk_{c['chunk_index']}",
                "text": c["text"],
            }
            for c in clauses
        ],
    )


@router.post("/risk", response_model=AnalyzeRiskResponse)
def analyze_risk(
    req: AnalyzeRiskRequest,
    embedder=Depends(get_embedder),
    agent=Depends(get_legal_agent),
    engines=Depends(get_risk_engine),
):
    # 1) Validate index_id exists.
    if not req.index_id:
        raise HTTPException(status_code=400, detail="index_id is required")

    classifier, scorer = engines

    index_dir = _resolve_uploaded_index_dir(req.index_id)

    # 2) Load FAISS index.
    try:
        index = VectorIndex.load(
            index_dir / "vectors.index",
            index_dir / "metadata.json",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load index for {req.index_id}: {exc}") from exc

    # 3) Run retrieval.
    try:
        query_embedding = embedder.encode([RISK_QUERY.strip()])
        clauses = index.search(query_embedding, top_k=req.top_k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Retrieval failed for {req.index_id}: {exc}") from exc

    if not clauses:
        return AnalyzeRiskResponse(
            risk_score=0,
            risk_level="LOW",
            clauses_analyzed=0,
            clauses=[],
        )

    clause_levels = []
    clause_outputs = []

    for clause in clauses:
        clause_text = clause["text"]

        # 4) Run Gemini analysis.
        try:
            analysis = agent.analyze_clause_risk(clause_text)
        except Exception as exc:
            analysis = _format_llm_error(exc)

        # 5) Run classifier.
        level = classifier.classify_clause(clause_text, analysis)
        clause_levels.append(level)

        clause_outputs.append(
            ClauseRisk(
                clause_id=clause.get(
                    "id",
                    f"page_{clause.get('page_number', 0)}_chunk_{clause.get('chunk_index', 0)}",
                ),
                text=clause_text,
                risk_level=level,
                reason=analysis,
            )
        )

    # 6) Aggregate score.
    doc_score = scorer.score(clause_levels)

    # 7) Return structured JSON.
    return AnalyzeRiskResponse(
        risk_score=doc_score["risk_score"],
        risk_level=doc_score["risk_level"],
        clauses_analyzed=doc_score["clauses_analyzed"],
        clauses=clause_outputs,
    )
