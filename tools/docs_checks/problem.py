"""The result type every check returns."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Problem:
    """One issue found in one file."""

    file: Path
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: {self.message}"
