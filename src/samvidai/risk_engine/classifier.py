class RiskClassifier:
    """
    Hybrid clause risk classifier.
    Deterministic rules + fallback to LLM text parsing.
    """

    LEVELS = ("HIGH", "MEDIUM", "LOW")

    KEYWORD_MAP = {
        "HIGH": ["HIGH", "CRITICAL", "SEVERE", "MAJOR", "SIGNIFICANT"],
        "MEDIUM": ["MEDIUM", "MODERATE", "ELEVATED", "SUBSTANTIAL"],
        "LOW": ["LOW", "MINOR", "NEGLIGIBLE", "MINIMAL"],
    }

    def rule_override(self, clause_text: str) -> str | None:
        text = clause_text.lower()

        if "unlimited liability" in text:
            return "HIGH"
        
        if "terminate at any time without cause" in text:
            return "HIGH"
        
        if "no indemnity cap" in text:
            return "HIGH"
        
        if "mutual termination" in text:
            return "LOW"
        
        return None
    
    def classify_clause(self, clause_text: str, analysis_text: str) -> str:
        # 1. Rule-based override
        rule_level = self.rule_override(clause_text)
        if rule_level:
            return rule_level
        
        # 2. Fallback to LLM output parsing
        text = analysis_text.upper()

        for level, keywords in self.KEYWORD_MAP.items():
            for kw in keywords:
                if kw in text:
                    return level
                
        return "LOW"