from tools.docs_checks.links import check_links


def test_valid_links_pass(docs):
    root = docs({
        "index.md": "[guide](guide/page.md) and [part](guide/page.md#second-part) and [self](#top)\n\n# Top\n",
        "guide/page.md": "# Page\n\n## Second part\n",
    })
    assert check_links(root) == []


def test_missing_file_is_reported(docs):
    root = docs({"index.md": "See [gone](missing.md).\n"})
    problems = check_links(root)
    assert len(problems) == 1
    assert problems[0].line == 1
    assert "missing file" in problems[0].message


def test_missing_anchor_is_reported(docs):
    root = docs({"index.md": "[x](other.md#nope)\n", "other.md": "# Other\n"})
    problems = check_links(root)
    assert [p.message for p in problems] == ["link to missing heading: other.md#nope"]


def test_external_links_and_code_are_ignored(docs):
    root = docs({"index.md": "[web](https://example.org)\n\n```\n[x](missing.md)\n```\n"})
    assert check_links(root) == []
