SYSTEM_RISK_PROMPT = """
You are a legal contract risk analysis engine.
Evaluate ONE clause and produce a stable, short output.
Use only these labels: LOW, MEDIUM, HIGH.
"""


def build_risk_prompt(clause_text: str) -> str:
    return f"""
{SYSTEM_RISK_PROMPT}

Rules:
1. Treat missing context as MEDIUM unless the clause clearly indicates LOW or HIGH.
2. Focus on legal exposure: liability, termination, indemnity, penalties, dispute terms, one-sided obligations.
3. Keep explanation to 1-2 sentences, maximum 60 words.
4. Output plain text only, no markdown, no extra sections.

Return EXACTLY this format:
Risk Level: <LOW|MEDIUM|HIGH>
Explanation: <short legal reason>

Clause:
<<<CLAUSE>>>
{clause_text}
<<<END_CLAUSE>>>
"""
