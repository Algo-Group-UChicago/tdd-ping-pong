from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Expense:
    payer: str
    # Prefer integers over floats due to floating point errors
    amount_cents: int
    participants: tuple[str, ...]
    description: str
    timestamp: datetime
