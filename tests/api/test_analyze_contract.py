from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_analyze_contract_empty_pdf():
    payload = {
        "pdf_path": "non_existent.pdf",
        "question": "termination"
    }
    resp = client.post("/analyze-contract", json=payload)
    assert resp.status_code in (400, 422, 500)  # expected failure