from tools.docs_checks.markdown import anchors, prose_lines, slugify


def test_slugify_matches_toc_style():
    assert slugify("Capture dates") == "capture-dates"
    assert slugify("Step 5 (optional): Score it") == "step-5-optional-score-it"
    assert slugify("  Making files load fast  ") == "making-files-load-fast"


def test_anchors_ignores_code_blocks():
    text = "# Title\n\n```bash\n# not a heading\n```\n\n## Real heading\n"
    assert anchors(text) == {"title", "real-heading"}


def test_prose_lines_skips_fenced_code_and_keeps_line_numbers():
    text = "one\n```\ncode\n```\nfive"
    assert list(prose_lines(text)) == [(1, "one"), (5, "five")]
