SYSTEM_RISK_PROMPT = """
You are a legal contract risk analysis engine.
Evaluate ONE clause and produce a stable, short JSON output.
Use only these labels: LOW, MEDIUM, HIGH.
"""


def build_risk_prompt(clause_text: str) -> str:
    return f"""
{SYSTEM_RISK_PROMPT}

Rules:
1. Treat missing context as MEDIUM unless the clause clearly indicates LOW or HIGH.
2. Focus on legal exposure: liability, termination, indemnity, penalties, dispute terms, one-sided obligations.
3. Keep explanation to 1-2 sentences, maximum 60 words.
4. Return STRICTLY valid JSON only.
5. No extra text. No markdown. No commentary.

Return EXACTLY this JSON schema:
{{
  "risk_level": "HIGH | MEDIUM | LOW",
  "reason": "Short explanation"
}}

Clause:
<<<CLAUSE>>>
{clause_text}
<<<END_CLAUSE>>>
"""
