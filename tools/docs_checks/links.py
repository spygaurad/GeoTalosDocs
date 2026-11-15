"""Check that every internal link points to an existing page and heading."""

import re
from functools import cache
from pathlib import Path

from .markdown import anchors, pages, prose_lines
from .problem import Problem

_LINK = re.compile(r"\]\(([^)\s]+)\)")
_EXTERNAL = ("http://", "https://", "mailto:")


@cache
def _anchors_of(page: Path) -> frozenset[str]:
    return frozenset(anchors(page.read_text(encoding="utf-8")))


def check_links(docs_dir: Path) -> list[Problem]:
    """Broken relative links and missing #anchors across all pages."""
    _anchors_of.cache_clear()  # pages may change between runs (tests, watch mode)
    problems: list[Problem] = []
    for page in pages(docs_dir):
        text = page.read_text(encoding="utf-8")
        for number, line in prose_lines(text):
            for target in _LINK.findall(line):
                if target.startswith(_EXTERNAL):
                    continue
                path_part, _, anchor = target.partition("#")
                target_file = (page.parent / path_part).resolve() if path_part else page.resolve()
                if not target_file.exists():
                    problems.append(Problem(page, number, f"link to missing file: {target}"))
                elif anchor and target_file.suffix == ".md" and anchor not in _anchors_of(target_file):
                    problems.append(Problem(page, number, f"link to missing heading: {target}"))
    return problems
