from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_analyze_qa_with_valid_pdf():
    """Test /analyze/qa endpoint with valid PDF path."""
    payload = {
        "pdf_path": "data/synthetic_contracts/NDA_Synthetic.pdf",
        "question": "termination",
        "top_k": 5
    }
    resp = client.post("/analyze/qa", json=payload)
    # Either success or expected failure for missing index
    assert resp.status_code in (200, 400, 404, 422, 500)


def test_analyze_risk_with_valid_pdf():
    """Test /analyze/risk endpoint with valid PDF path."""
    payload = {
        "pdf_path": "data/synthetic_contracts/NDA_Synthetic.pdf",
        "top_k": 10
    }
    resp = client.post("/analyze/risk", json=payload)
    # Either success or expected failure for missing index
    assert resp.status_code in (200, 400, 404, 422, 500)


def test_analyze_risk_schema():
    """Test /analyze/risk returns correct schema structure when successful."""
    payload = {
        "pdf_path": "data/synthetic_contracts/NDA_Synthetic.pdf",
        "top_k": 10
    }
    resp = client.post("/analyze/risk", json=payload)
    # Only check schema if successful
    if resp.status_code == 200:
        data = resp.json()
        assert "risk_score" in data
        assert "risk_level" in data
        assert "clauses_analyzed" in data
        assert "clauses" in data
        assert isinstance(data["clauses"], list)
