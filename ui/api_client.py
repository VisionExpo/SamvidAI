import os
import requests

API_BASE = os.getenv("SAMVID_API_URL", "http://localhost:8000")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"


def analyze_contract(pdf_path: str, top_k: int = 10):
    """
    Analyze contract risk via API.
    
    Args:
        pdf_path: Path to the PDF contract file
        top_k: Number of top clauses to retrieve for analysis
        
    Returns:
        dict with risk_score, risk_level, clauses_analyzed, clauses
    """
    if MOCK_MODE:
        return {
            "risk_score": 72,
            "risk_level": "HIGH",
            "clauses_analyzed": 3,
            "clauses": [
                {
                    "clause_id": "page_1_chunk_1",
                    "text": "Unilateral termination clause",
                    "risk_level": "HIGH",
                    "reason": "Allows termination without cause"
                },
                {
                    "clause_id": "page_1_chunk_2",
                    "text": "Missing indemnity cap",
                    "risk_level": "HIGH",
                    "reason": "No limit on indemnity obligations"
                },
                {
                    "clause_id": "page_2_chunk_1",
                    "text": "Jurisdiction favors counterparty",
                    "risk_level": "MEDIUM",
                    "reason": "Legal disputes resolved in foreign jurisdiction"
                }
            ]
        }

    resp = requests.post(
        f"{API_BASE}/analyze/risk",
        json={"pdf_path": pdf_path, "top_k": top_k},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()
