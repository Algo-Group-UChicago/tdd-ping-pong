"""Test doubles you can inject into a Ledger instead of the real thing."""

from datetime import datetime, timedelta


class FakeClock:
    """A clock that only moves when the test tells it to.

    Pass it anywhere a `clock` is expected: calling it returns the current
    fake time, just like calling datetime.now() would.
    """

    def __init__(self, now: datetime) -> None:
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def set(self, dt: datetime) -> None:
        self.now = dt

    def advance(self, delta: timedelta) -> None:
        self.now += delta


class InMemoryStorage:
    """Implements the Storage protocol with a list instead of a file."""

    def __init__(self, records: list[dict] | None = None) -> None:
        self.records: list[dict] = list(records or [])
        self.save_calls = 0

    def save(self, records: list[dict]) -> None:
        self.records = [dict(r) for r in records]
        self.save_calls += 1

    def load(self) -> list[dict]:
        return [dict(r) for r in self.records]
