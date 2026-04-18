"""Unit tests for scripts/ask_server.py — pure utility functions only."""

import json

import ask_server
from ask_server import (
    _build_structured_prompt,
    _load_session,
    _normalize_question,
    _save_session,
    _strip_frontmatter,
)


# ── Question normalization ───────────────────────────────────────────


class TestNormalizeQuestion:
    def test_lowercase(self):
        assert _normalize_question("What Is GStack?") == "what is gstack?"

    def test_em_dash_normalized(self):
        assert _normalize_question("who\u2014garrytan") == "who-garrytan"

    def test_en_dash_normalized(self):
        assert _normalize_question("who\u2013garrytan") == "who-garrytan"

    def test_smart_quotes_normalized(self):
        result = _normalize_question("what\u2019s")
        assert result == "what's"

    def test_whitespace_collapsed(self):
        assert _normalize_question("  too   many   spaces  ") == "too many spaces"

    def test_empty_string(self):
        assert _normalize_question("") == ""

    def test_already_normalized(self):
        assert _normalize_question("simple question") == "simple question"


# ── Frontmatter stripping ────────────────────────────────────────────


class TestStripFrontmatter:
    def test_with_frontmatter(self):
        text = "---\ntitle: X\n---\nContent here"
        assert _strip_frontmatter(text) == "Content here"

    def test_without_frontmatter(self):
        text = "Just plain content"
        assert _strip_frontmatter(text) == "Just plain content"

    def test_empty_string(self):
        assert _strip_frontmatter("") == ""

    def test_frontmatter_only(self):
        text = "---\ntitle: X\n---\n"
        assert _strip_frontmatter(text) == ""

    def test_triple_dash_not_at_start(self):
        text = "Some text\n---\ntitle: X\n---\nMore"
        assert _strip_frontmatter(text) == text

    def test_incomplete_frontmatter(self):
        text = "---\ntitle: X\nno closing dashes"
        assert _strip_frontmatter(text) == text


# ── Session persistence ──────────────────────────────────────────────


class TestSessionPersistence:
    def test_save_and_load_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ask_server, "SESSIONS_DIR", tmp_path)
        _save_session("sess-1", "token-abc")
        result = _load_session("sess-1")
        assert result == "token-abc"

    def test_load_nonexistent_session(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ask_server, "SESSIONS_DIR", tmp_path)
        assert _load_session("does-not-exist") is None

    def test_load_corrupt_json(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ask_server, "SESSIONS_DIR", tmp_path)
        (tmp_path / "bad.json").write_text("not json{{{")
        assert _load_session("bad") is None

    def test_load_missing_resume_key(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ask_server, "SESSIONS_DIR", tmp_path)
        (tmp_path / "nokey.json").write_text(json.dumps({"session_id": "nokey"}))
        assert _load_session("nokey") is None


# ── Structured prompt building ───────────────────────────────────────


class TestBuildStructuredPrompt:
    def _setup_wiki(self, tmp_path, monkeypatch):
        """Create minimal fake wiki files and point PROJECT_ROOT at tmp_path."""
        monkeypatch.setattr(ask_server, "PROJECT_ROOT", tmp_path)
        reports_dir = tmp_path / "wiki" / "reports"
        reports_dir.mkdir(parents=True)
        (reports_dir / "2026-04-16-morning-briefing.md").write_text(
            "---\ntitle: Briefing\n---\n# Morning Briefing\nContent here"
        )
        patterns_dir = tmp_path / "wiki" / "patterns"
        patterns_dir.mkdir(parents=True)
        (patterns_dir / "burnout-signals.md").write_text(
            "---\ntitle: Burnout\n---\n# Burnout Signals\nDetails"
        )
        (patterns_dir / "review-bottleneck.md").write_text(
            "---\ntitle: Bottleneck\n---\n# Review Bottleneck\nDetails"
        )
        (patterns_dir / "stuck-items-growth.md").write_text(
            "---\ntitle: Stuck\n---\n# Stuck Items Growth\nDetails"
        )
        connections_dir = tmp_path / "wiki" / "connections"
        connections_dir.mkdir(parents=True)
        (connections_dir / "sole-maintainer-and-stuck-growth.md").write_text(
            "---\ntitle: Connection\n---\n# Connection\nDetails"
        )
        projects_dir = tmp_path / "wiki" / "projects"
        projects_dir.mkdir(parents=True)
        (projects_dir / "gstack.md").write_text(
            "---\ntitle: gstack\n---\n# gstack\nDetails"
        )
        (projects_dir / "autoresearch.md").write_text(
            "---\ntitle: autoresearch\n---\n# autoresearch\nDetails"
        )

    def test_morning_briefing_match(self, tmp_path, monkeypatch):
        self._setup_wiki(tmp_path, monkeypatch)
        result = _build_structured_prompt("What is the morning briefing?")
        assert result is not None
        prompt, paths, status = result
        assert any("morning-briefing" in p for p in paths)

    def test_burnout_risk_match(self, tmp_path, monkeypatch):
        self._setup_wiki(tmp_path, monkeypatch)
        result = _build_structured_prompt("Who has the highest burnout risk?")
        assert result is not None
        _, paths, _ = result
        assert any("burnout" in p for p in paths)

    def test_compare_repos_match(self, tmp_path, monkeypatch):
        self._setup_wiki(tmp_path, monkeypatch)
        result = _build_structured_prompt("Compare gstack and autoresearch")
        assert result is not None
        _, paths, _ = result
        assert any("gstack" in p for p in paths)
        assert any("autoresearch" in p for p in paths)

    def test_unrecognized_question_returns_none(self, tmp_path, monkeypatch):
        self._setup_wiki(tmp_path, monkeypatch)
        result = _build_structured_prompt("What is the weather today?")
        assert result is None

    def test_no_docs_exist_returns_none(self, tmp_path, monkeypatch):
        # Point to empty tmp_path — no wiki files exist
        monkeypatch.setattr(ask_server, "PROJECT_ROOT", tmp_path)
        result = _build_structured_prompt("What is the morning briefing?")
        assert result is None
