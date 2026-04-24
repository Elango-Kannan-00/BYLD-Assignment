from enum import Enum


class RiskProfile(str, Enum):
    conservative = "conservative"
    balanced = "balanced"
    aggressive = "aggressive"
