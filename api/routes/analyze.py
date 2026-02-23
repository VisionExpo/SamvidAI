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
    {
        "clause_id": f"page_{c['page_number']}_chunk_{c['chunk_index']}",
        "text": c["text"],
    }
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

    # Use centralized risk query
    query_embedding = embedder.encode([RISK_QUERY.strip()])

    clauses = index.search(query_embedding, top_k=req.top_k)

    # Handle empty retrieval
    if not clauses:
        return AnalyzeRiskResponse(
            risk_score=0,
            risk_level="LOW",
            clauses_analyzed=0,
            clauses=[]
        )

    clause_levels = []
    clause_outputs = []

    for clause in clauses:
        clause_text = clause["text"]

        # 1️⃣ LLM analysis with failure handling
        try:
            analysis = agent.analyze_clause_risk(clause_text)
        except Exception as e:
            analysis = "LLM analysis failed. Defaulting to LOW risk."

        # 2️⃣ Hybrid classification
        level = classifier.classify_clause(clause_text, analysis)

        clause_levels.append(level)

        clause_outputs.append(
            ClauseRisk(
                clause_id=clause.get("id", f"page_{clause.get('page_number', 0)}_chunk_{clause.get('chunk_index', 0)}"),
                text=clause_text,
                risk_level=level,
                reason=analysis,
            )
        )

    # 3️⃣ Document-level scoring
    doc_score = scorer.score(clause_levels)

    return AnalyzeRiskResponse(
        risk_score=doc_score["risk_score"],
        risk_level=doc_score["risk_level"],
        clauses_analyzed=doc_score["clauses_analyzed"],
        clauses=clause_outputs,
    )
