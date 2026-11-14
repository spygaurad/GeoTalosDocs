from tools.docs_checks.cli import main


def test_clean_docs_exit_zero(docs, capsys):
    root = docs({"index.md": "# Home\n\n[self](#home)\n"})
    assert main([str(root)]) == 0
    assert "0 problem(s)" in capsys.readouterr().out


def test_problems_exit_one_and_are_printed(docs, capsys):
    root = docs({"index.md": "[x](gone.md)\n"})
    assert main([str(root)]) == 1
    assert "missing file" in capsys.readouterr().out


def test_missing_docs_dir_exits_two(tmp_path):
    assert main([str(tmp_path / "nope")]) == 2
