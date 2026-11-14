"""Command line entry: run every check and exit non-zero on any problem.

Usage: python -m tools.docs_checks [docs_dir]
"""

import sys
from collections.abc import Callable
from pathlib import Path

from .content import check_dashes, check_placeholders
from .links import check_links
from .problem import Problem

CHECKS: dict[str, Callable[[Path], list[Problem]]] = {
    "links": check_links,
    "placeholders": check_placeholders,
    "dashes": check_dashes,
}


def run(docs_dir: Path) -> list[Problem]:
    """Run all checks and return every problem found."""
    return [problem for check in CHECKS.values() for problem in check(docs_dir)]


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    docs_dir = Path(args[0]) if args else Path("docs")
    if not docs_dir.is_dir():
        print(f"docs directory not found: {docs_dir}", file=sys.stderr)
        return 2
    problems = run(docs_dir)
    for problem in problems:
        print(problem)
    print(f"{len(problems)} problem(s) in {docs_dir}")
    return 1 if problems else 0
