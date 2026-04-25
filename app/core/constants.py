from enum import Enum


class RiskProfile(str, Enum):
    conservative = "conservative"
    balanced = "balanced"
    aggressive = "aggressive"


class TransactionType(str, Enum):
    buy = "buy"
    sell = "sell"
