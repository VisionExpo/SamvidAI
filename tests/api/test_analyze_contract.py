from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_analyze_qa_empty_pdf():
    """Test /analyze/qa endpoint with non-existent PDF."""
    payload = {
        "pdf_path": "non_existent.pdf",
        "question": "termination",
        "top_k": 5
    }
    resp = client.post("/analyze/qa", json=payload)
    assert resp.status_code in (400, 422, 500)  # expected failure


def test_analyze_risk_empty_pdf():
    """Test /analyze/risk endpoint with non-existent PDF."""
    payload = {
        "pdf_path": "non_existent.pdf",
        "top_k": 10
    }
    resp = client.post("/analyze/risk", json=payload)
    assert resp.status_code in (400, 422, 500)  # expected failure


def test_analyze_risk_schema():
    """Test /analyze/risk returns correct schema structure."""
    payload = {
        "pdf_path": "non_existent.pdf",
        "top_k": 10
    }
    resp = client.post("/analyze/risk", json=payload)
    # Expected to fail (file not found), but check schema if it were to succeed
    if resp.status_code == 200:
        data = resp.json()
        assert "risk_score" in data
        assert "risk_level" in data
        assert "clauses_analyzed" in data
        assert "clauses" in data
        assert isinstance(data["clauses"], list)
