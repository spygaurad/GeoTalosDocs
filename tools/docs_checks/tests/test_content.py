from tools.docs_checks.content import PLACEHOLDER_TEXT, check_dashes, check_placeholders


def test_placeholder_page_is_reported(docs):
    root = docs({"done.md": "# Done\n", "todo.md": f"# Todo\n\n{PLACEHOLDER_TEXT}.\n"})
    problems = check_placeholders(root)
    assert [p.file.name for p in problems] == ["todo.md"]


def test_em_and_en_dashes_are_reported(docs):
    root = docs({"a.md": "One — two\nRange 1–2\nfine line\n"})
    assert [p.line for p in check_dashes(root)] == [1, 2]


def test_spaced_hyphen_is_reported_but_list_items_are_not(docs):
    root = docs({"a.md": "- a list item\nword - word\n"})
    problems = check_dashes(root)
    assert [(p.line, p.message) for p in problems] == [(2, "spaced hyphen used as a dash")]


def test_dashes_in_code_are_ignored(docs):
    root = docs({"a.md": "Run `a - b` here\n\n```\nx — y\n```\n"})
    assert check_dashes(root) == []
