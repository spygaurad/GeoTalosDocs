"""Check that every internal link points to an existing page and heading."""

import re
from pathlib import Path

from .markdown import anchors, pages, prose_lines
from .problem import Problem

_LINK = re.compile(r"\]\(([^)\s]+)\)")
_EXTERNAL = ("http://", "https://", "mailto:")


def check_links(docs_dir: Path) -> list[Problem]:
    """Broken relative links and missing #anchors across all pages."""
    problems: list[Problem] = []
    anchor_cache: dict[Path, set[str]] = {}

    def anchors_of(page: Path) -> set[str]:
        if page not in anchor_cache:
            anchor_cache[page] = anchors(page.read_text(encoding="utf-8"))
        return anchor_cache[page]

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
                elif anchor and target_file.suffix == ".md" and anchor not in anchors_of(target_file):
                    problems.append(Problem(page, number, f"link to missing heading: {target}"))
    return problems
