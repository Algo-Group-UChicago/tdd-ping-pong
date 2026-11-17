"""Persistence for plain records (lists of dicts).
"""

import json
from pathlib import Path
from typing import Protocol


class Storage(Protocol):
    """Anything with these two methods can be handed to a Ledger."""

    def save(self, records: list[dict]) -> None: ...

    def load(self) -> list[dict]: ...


class JsonFileStorage:
    """Stores records as a JSON array in a file on disk."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def save(self, records: list[dict]) -> None:
        self.path.write_text(json.dumps(records, indent=2))

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text())
