import os
import io
import requests
from typing import Union

API_BASE = os.getenv("SAMVID_API_URL", "http://localhost:8000")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"


def upload_contract(file: Union[io.BytesIO, bytes], filename: str, data_source: str = "govt_contracts"):
    """
    Upload a contract PDF to the API.
    
    Args:
        file: The PDF file content (BytesIO or bytes)
        filename: Name of the PDF file
        data_source: Target directory in data folder (default: govt_contracts)
        
    Returns:
        dict with status, filename, data_source
    """
    if MOCK_MODE:
        return {
            "status": "uploaded",
            "filename": filename,
            "data_source": data_source,
        }

    files = {"file": (filename, file, "application/pdf")}
    data = {"data_source": data_source}
    
    resp = requests.post(
        f"{API_BASE}/upload",
        files=files,
        data=data,
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()


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


def analyze_contract_from_upload(file: Union[io.BytesIO, bytes], filename: str, top_k: int = 10, data_source: str = "govt_contracts"):
    """
    Upload a contract PDF and analyze its risk.
    
    Args:
        file: The PDF file content (BytesIO or bytes)
        filename: Name of the PDF file
        top_k: Number of top clauses to retrieve for analysis
        data_source: Target directory in data folder (default: govt_contracts)
        
    Returns:
        dict with risk_score, risk_level, clauses_analyzed, clauses
    """
    # First upload the file
    upload_result = upload_contract(file, filename, data_source)
    
    # Get the saved path
    saved_path = f"data/{upload_result['data_source']}/{upload_result['filename']}"
    
    # Then analyze
    return analyze_contract(saved_path, top_k=top_k)
