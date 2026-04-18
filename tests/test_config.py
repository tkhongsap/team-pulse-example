"""Unit tests for scripts/config.py — shared configuration."""

import re
from datetime import datetime, timedelta, timezone

from config import PROJECT_ROOT, TZ, now_local, today_local


# ── now_local ────────────────────────────────────────────────────────


class TestNowLocal:
    def test_returns_datetime_with_tz(self):
        result = now_local()
        assert isinstance(result, datetime)
        assert result.tzinfo is not None

    def test_timezone_offset(self):
        result = now_local()
        assert result.utcoffset() == TZ.utcoffset(None)


# ── today_local ──────────────────────────────────────────────────────


class TestTodayLocal:
    def test_returns_date_string_format(self):
        result = today_local()
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", result)

    def test_matches_now_local_date(self):
        assert today_local() == now_local().strftime("%Y-%m-%d")


# ── Config constants ─────────────────────────────────────────────────


class TestConfigConstants:
    def test_project_root_exists(self):
        assert PROJECT_ROOT.is_dir()

    def test_tz_default_offset(self):
        # Default TZ is UTC+7 (Bangkok)
        expected = timezone(timedelta(hours=7))
        assert TZ.utcoffset(None) == expected.utcoffset(None)
