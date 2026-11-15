from pathlib import Path

import pytest


@pytest.fixture
def docs(tmp_path: Path):
    """Build a small docs tree: docs({"index.md": "...", "a/b.md": "..."})."""

    def make(files: dict[str, str]) -> Path:
        for name, text in files.items():
            path = tmp_path / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return tmp_path

    return make
