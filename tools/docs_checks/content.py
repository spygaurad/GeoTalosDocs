"""Content rules for the docs text.

- No placeholder pages left from the scaffold.
- No em dashes, en dashes or spaced hyphens used as dashes in prose
  (house style: use a period, comma, colon or parentheses instead).
"""

import re
from pathlib import Path

from .markdown import pages, prose_lines
from .problem import Problem

PLACEHOLDER_TEXT = "This page is a placeholder"
_DASHES = re.compile("[–—]")
_SPACED_HYPHEN = re.compile(r"\S - \S")
_LIST_ITEM = re.compile(r"^\s*[-*+] ")


def check_placeholders(docs_dir: Path) -> list[Problem]:
    """Pages that still contain the scaffold's placeholder note."""
    problems = []
    for page in pages(docs_dir):
        for number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), start=1):
            if PLACEHOLDER_TEXT in line:
                problems.append(Problem(page, number, "placeholder page, content missing"))
    return problems


def check_dashes(docs_dir: Path) -> list[Problem]:
    """Em/en dashes and ' - ' used as a dash, outside code blocks and inline code."""
    problems = []
    for page in pages(docs_dir):
        for number, line in prose_lines(page.read_text(encoding="utf-8")):
            prose = re.sub(r"`[^`]*`", "", line)
            if _DASHES.search(prose):
                problems.append(Problem(page, number, "em or en dash"))
            elif _SPACED_HYPHEN.search(_LIST_ITEM.sub("", prose)):
                problems.append(Problem(page, number, "spaced hyphen used as a dash"))
    return problems
