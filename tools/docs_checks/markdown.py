"""Small helpers for reading Markdown pages.

Kept separate so the link and content checks share one definition of
"prose" (text outside fenced code blocks) and of heading anchors.
"""

import re
import unicodedata
from collections.abc import Iterator
from pathlib import Path

_FENCE = re.compile(r"^\s*(```|~~~)")
_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")


def pages(docs_dir: Path) -> list[Path]:
    """All Markdown files under docs_dir, sorted for stable output."""
    return sorted(docs_dir.rglob("*.md"))


def prose_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield (line number, line) for lines outside fenced code blocks."""
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield number, line


def slugify(heading: str) -> str:
    """Turn a heading into its anchor, the same way Python-Markdown's toc does."""
    value = unicodedata.normalize("NFKD", heading).encode("ascii", "ignore").decode()
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def anchors(text: str) -> set[str]:
    """Anchors of all headings on a page."""
    return {
        slugify(match.group(1))
        for _, line in prose_lines(text)
        if (match := _HEADING.match(line))
    }
