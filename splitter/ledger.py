from datetime import datetime
from typing import Callable

from splitter.models import Expense
from splitter.storage import Storage


class Ledger:
    """Tracker for shared expenses between roommates.

    Dependencies:
      - clock: any zero-argument callable that returns a datetime. 
      Defaults to datetime.now() if none is provided.
      - storage: any object with save(records) and load() (see storage.py).
    """

    def __init__(
        self,
        clock: Callable[[], datetime] = datetime.now,
        storage: Storage | None = None,
    ) -> None:
        self._clock = clock
        self._storage = storage
        self._expenses: list[Expense] = []

    def add_expense(
        self,
        payer: str,
        amount_cents: int,
        participants: list[str] | tuple[str, ...],
        description: str,
    ) -> Expense:
        if not payer:
            raise ValueError("payer must not be empty")
        if amount_cents <= 0:
            raise ValueError("amount_cents must be positive")
        if not participants:
            raise ValueError("participants must not be empty")

        expense = Expense(
            payer=payer,
            amount_cents=amount_cents,
            participants=tuple(participants),
            description=description,
            timestamp=self._clock(),
        )
        self._expenses.append(expense)
        return expense

    @property
    def expenses(self) -> list[Expense]:
        return list(self._expenses)
