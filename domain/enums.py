from enum import Enum


class ClauseType(str, Enum):
    TERMINATION = "termination"
    LIABILITY = "liability"
    PAYMENT = "payment"
    CONFIDENTIALITY = "confidentiality"
    GOVERNING_LAW = "governing_law"
    OTHER = "other"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
