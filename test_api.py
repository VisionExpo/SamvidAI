import requests
import json

# Test the risk analysis endpoint with existing index
payload = {
    "pdf_path": "data/synthetic_contracts/NDA_Synthetic.pdf",
    "top_k": 5
}

try:
    r = requests.post('http://localhost:8000/analyze/risk', json=payload, timeout=60)
    print('Status:', r.status_code)
    if r.status_code == 200:
        result = r.json()
        print('Success!')
        print('Risk Score:', result.get('risk_score'))
        print('Risk Level:', result.get('risk_level'))
        print('Clauses Analyzed:', result.get('clauses_analyzed'))
        print('Clauses:')
        for c in result.get('clauses', [])[:3]:
            print(f"  - {c.get('clause_id')}: {c.get('risk_level')}")
    else:
        print('Error:', r.text[:500])
except Exception as e:
    print('Exception:', str(e))
