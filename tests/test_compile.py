"""Unit tests for scripts/compile.py — wiki compilation logic."""

import compile as compile_mod
from compile import build_prompt, find_uncompiled, get_compiled_files, get_raw_files


# ── get_raw_files ────────────────────────────────────────────────────


class TestGetRawFiles:
    def test_empty_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr(compile_mod, "RAW_DIR", tmp_path)
        assert get_raw_files() == []

    def test_returns_sorted_md_files(self, tmp_path, monkeypatch):
        monkeypatch.setattr(compile_mod, "RAW_DIR", tmp_path)
        (tmp_path / "2026-04-05-pm.md").touch()
        (tmp_path / "2026-04-04-am.md").touch()
        result = get_raw_files()
        assert result == ["2026-04-04-am.md", "2026-04-05-pm.md"]

    def test_ignores_non_md_files(self, tmp_path, monkeypatch):
        monkeypatch.setattr(compile_mod, "RAW_DIR", tmp_path)
        (tmp_path / "2026-04-04-am.md").touch()
        (tmp_path / "notes.txt").touch()
        (tmp_path / "data.json").touch()
        result = get_raw_files()
        assert result == ["2026-04-04-am.md"]

    def test_nonexistent_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr(compile_mod, "RAW_DIR", tmp_path / "nonexistent")
        assert get_raw_files() == []


# ── get_compiled_files ───────────────────────────────────────────────


class TestGetCompiledFiles:
    def test_no_log_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(compile_mod, "WIKI_LOG", tmp_path / "nope.md")
        assert get_compiled_files() == set()

    def test_explicit_file_refs(self, tmp_path, monkeypatch):
        log = tmp_path / "log.md"
        log.write_text("- Sources: raw/github-daily/2026-04-12-am.md\n")
        monkeypatch.setattr(compile_mod, "WIKI_LOG", log)
        result = get_compiled_files()
        assert "2026-04-12-am.md" in result

    def test_through_range_expansion(self, tmp_path, monkeypatch):
        log = tmp_path / "log.md"
        log.write_text(
            "raw/github-daily/2026-04-04-am.md through raw/github-daily/2026-04-06-pm.md"
        )
        monkeypatch.setattr(compile_mod, "WIKI_LOG", log)
        result = get_compiled_files()
        expected = {
            "2026-04-04-am.md", "2026-04-04-pm.md",
            "2026-04-05-am.md", "2026-04-05-pm.md",
            "2026-04-06-am.md", "2026-04-06-pm.md",
        }
        assert expected.issubset(result)

    def test_mixed_explicit_and_range(self, tmp_path, monkeypatch):
        log = tmp_path / "log.md"
        log.write_text(
            "raw/github-daily/2026-04-04-am.md through raw/github-daily/2026-04-05-pm.md\n"
            "Sources: raw/github-daily/2026-04-10-am.md\n"
        )
        monkeypatch.setattr(compile_mod, "WIKI_LOG", log)
        result = get_compiled_files()
        assert "2026-04-04-am.md" in result
        assert "2026-04-05-pm.md" in result
        assert "2026-04-10-am.md" in result

    def test_empty_log_file(self, tmp_path, monkeypatch):
        log = tmp_path / "log.md"
        log.write_text("")
        monkeypatch.setattr(compile_mod, "WIKI_LOG", log)
        assert get_compiled_files() == set()


# ── find_uncompiled ──────────────────────────────────────────────────


class TestFindUncompiled:
    def test_all_compiled(self, tmp_path, monkeypatch):
        raw_dir = tmp_path / "raw"
        raw_dir.mkdir()
        monkeypatch.setattr(compile_mod, "RAW_DIR", raw_dir)
        (raw_dir / "2026-04-04-am.md").touch()
        log = tmp_path / "log.md"
        log.write_text("raw/github-daily/2026-04-04-am.md\n")
        monkeypatch.setattr(compile_mod, "WIKI_LOG", log)
        assert find_uncompiled() == []

    def test_some_uncompiled(self, tmp_path, monkeypatch):
        raw_dir = tmp_path / "raw"
        raw_dir.mkdir()
        monkeypatch.setattr(compile_mod, "RAW_DIR", raw_dir)
        (raw_dir / "2026-04-04-am.md").touch()
        (raw_dir / "2026-04-05-am.md").touch()
        log = tmp_path / "log.md"
        log.write_text("raw/github-daily/2026-04-04-am.md\n")
        monkeypatch.setattr(compile_mod, "WIKI_LOG", log)
        result = find_uncompiled()
        assert result == ["2026-04-05-am.md"]

    def test_date_filter(self, tmp_path, monkeypatch):
        monkeypatch.setattr(compile_mod, "RAW_DIR", tmp_path)
        (tmp_path / "2026-04-04-am.md").touch()
        (tmp_path / "2026-04-10-am.md").touch()
        monkeypatch.setattr(compile_mod, "WIKI_LOG", tmp_path / "nope.md")
        result = find_uncompiled("2026-04-10")
        assert result == ["2026-04-10-am.md"]

    def test_date_filter_no_match(self, tmp_path, monkeypatch):
        monkeypatch.setattr(compile_mod, "RAW_DIR", tmp_path)
        (tmp_path / "2026-04-04-am.md").touch()
        monkeypatch.setattr(compile_mod, "WIKI_LOG", tmp_path / "nope.md")
        result = find_uncompiled("2026-04-20")
        assert result == []

    def test_no_raw_files(self, tmp_path, monkeypatch):
        monkeypatch.setattr(compile_mod, "RAW_DIR", tmp_path)
        monkeypatch.setattr(compile_mod, "WIKI_LOG", tmp_path / "nope.md")
        assert find_uncompiled() == []


# ── build_prompt ─────────────────────────────────────────────────────


class TestBuildPrompt:
    def test_single_file(self):
        prompt = build_prompt(["2026-04-10-am.md"])
        assert "raw/github-daily/2026-04-10-am.md" in prompt

    def test_multiple_files(self):
        files = ["2026-04-10-am.md", "2026-04-10-pm.md"]
        prompt = build_prompt(files)
        assert "2026-04-10-am.md" in prompt
        assert "2026-04-10-pm.md" in prompt

    def test_instructions_present(self):
        prompt = build_prompt(["2026-04-10-am.md"])
        assert "wiki/log.md" in prompt
        assert "wiki/index.md" in prompt
        assert "Accumulate, don't replace" in prompt

    def test_empty_files_list(self):
        prompt = build_prompt([])
        # Still structurally valid — instructions are present
        assert "wiki/log.md" in prompt
