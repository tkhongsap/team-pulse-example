"""Unit tests for scripts/generate_report.py prompt structure."""

from generate_report import (
    build_dashboard_prompt,
    build_eod_prompt,
    build_morning_prompt,
)


class TestMorningPrompt:
    def test_includes_new_section_order(self):
        prompt = build_morning_prompt("2026-04-18")
        assert "Top-Line Summary" in prompt
        assert "What Changed Since Yesterday" in prompt
        assert "Top 3 Unblockers" in prompt
        assert "Urgent Today" in prompt
        assert "Review Soon" in prompt
        assert "Watchlist" in prompt
        assert "New Overnight Signals" in prompt
        assert "Recommended Actions Today" in prompt

    def test_includes_operational_constraints(self):
        prompt = build_morning_prompt("2026-04-18")
        assert "team leads" in prompt
        assert "critical" in prompt
        assert "high" in prompt
        assert "medium" in prompt
        assert "watch" in prompt
        assert "Backlog" in prompt
        assert "Ready to Hand Off" in prompt
        assert "Owner" in prompt
        assert "Next step" in prompt
        assert "Due window" in prompt
        assert "Why now" in prompt


class TestEodPrompt:
    def test_includes_scoreboard_sections(self):
        prompt = build_eod_prompt("2026-04-16")
        assert "Top-Line Summary" in prompt
        assert "Morning Commitments vs Actual Outcomes" in prompt
        assert "Resolved Today" in prompt
        assert "Newly Stuck Today" in prompt
        assert "Proof of Progress" in prompt
        assert "Carry-Over to Tomorrow" in prompt
        assert "Tomorrow's First Moves" in prompt

    def test_includes_shared_vocabulary(self):
        prompt = build_eod_prompt("2026-04-16")
        assert "critical" in prompt
        assert "high" in prompt
        assert "medium" in prompt
        assert "watch" in prompt
        assert "Backlog" in prompt
        assert "In Progress" in prompt
        assert "Stuck" in prompt
        assert "Ready to Hand Off" in prompt


class TestDashboardPrompt:
    def test_includes_manager_first_sections(self):
        prompt = build_dashboard_prompt("2026-04-18")
        assert "Top-Line Summary" in prompt
        assert "Team Health Score" in prompt
        assert "Repo Health Split" in prompt
        assert "Top Risks" in prompt
        assert "Top Manager Actions" in prompt
        assert "Key Metrics vs Targets" in prompt
        assert "Needs Help Now" in prompt
        assert "Monitor This Week" in prompt
        assert "Confidence / Freshness" in prompt

    def test_includes_team_lead_guidance(self):
        prompt = build_dashboard_prompt("2026-04-18")
        assert "team leads" in prompt
        assert "current value, target, and trend direction" in prompt
        assert "complete, partial, or using fallback/limited data" in prompt
