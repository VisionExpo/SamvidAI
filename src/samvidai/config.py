"""
Centralized configuration for SamvidAI
"""

# Risk query for semantic retrieval of risky clauses
# Used in Phase 2 - Retrieval Stabilization
RISK_QUERY = """
termination indemnity liability penalty damages breach
arbitration governing law force majeure confidentiality
"""

# Default top_k for retrieval
DEFAULT_TOP_K = 10

# Risk score thresholds
RISK_THRESHOLDS = {
    "HIGH": 70,
    "MEDIUM": 40,
    "LOW": 0,
}
