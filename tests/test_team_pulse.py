"""Unit tests for scripts/team_pulse.py — core GitHub data extraction."""

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from conftest import make_issue, make_pr, make_repo_data

from team_pulse import (
    _format_duration,
    _label_str,
    _parse_ts,
    aggregate_workload_by_assignee,
    filter_issues_by_date,
    filter_prs_by_date,
    generate_report,
)


# ── Timestamp parsing ────────────────────────────────────────────────


class TestParseTs:
    def test_valid_iso_utc(self):
        result = _parse_ts("2026-04-10T14:30:00Z")
        assert result is not None
        assert result.year == 2026
        assert result.month == 4
        assert result.day == 10
        assert result.hour == 14
        assert result.minute == 30

    def test_valid_iso_with_offset(self):
        result = _parse_ts("2026-04-10T14:30:00+07:00")
        assert result is not None
        assert result.hour == 14

    def test_none_input(self):
        assert _parse_ts(None) is None

    def test_empty_string(self):
        assert _parse_ts("") is None

    def test_malformed_string(self):
        assert _parse_ts("not-a-date") is None

    def test_iso_with_fractional_seconds(self):
        result = _parse_ts("2026-04-10T14:30:00.123456Z")
        assert result is not None
        assert result.second == 0
        assert result.microsecond == 123456


# ── Duration formatting ──────────────────────────────────────────────


class TestFormatDuration:
    def test_zero_hours(self):
        assert _format_duration(0) == "0m"

    def test_under_one_hour(self):
        assert _format_duration(0.5) == "30m"

    def test_boundary_one_hour(self):
        assert _format_duration(1.0) == "1.0h"

    def test_several_hours(self):
        assert _format_duration(5.5) == "5.5h"

    def test_boundary_24_hours(self):
        assert _format_duration(24.0) == "1.0d"

    def test_multiple_days(self):
        assert _format_duration(72.0) == "3.0d"

    def test_fractional_minutes(self):
        assert _format_duration(0.1) == "6m"

    def test_just_under_one_hour(self):
        assert _format_duration(0.99) == "59m"

    def test_just_under_24_hours(self):
        assert _format_duration(23.9) == "23.9h"


# ── PR filtering ─────────────────────────────────────────────────────


class TestFilterPrsByDate:
    def test_empty_list(self):
        opened, merged, open_prs = filter_prs_by_date([], "2026-04-10")
        assert opened == []
        assert merged == []
        assert open_prs == []

    def test_pr_opened_today(self):
        pr = make_pr(created_at="2026-04-10T10:00:00Z", state="open")
        opened, _, _ = filter_prs_by_date([pr], "2026-04-10")
        assert len(opened) == 1
        assert opened[0]["number"] == 1

    def test_pr_opened_different_day(self):
        pr = make_pr(created_at="2026-04-09T10:00:00Z", state="open")
        opened, _, _ = filter_prs_by_date([pr], "2026-04-10")
        assert opened == []

    def test_pr_merged_today(self):
        pr = make_pr(
            created_at="2026-04-08T10:00:00Z",
            merged_at="2026-04-10T15:00:00Z",
            state="closed",
            merged_by={"login": "reviewer"},
        )
        _, merged, _ = filter_prs_by_date([pr], "2026-04-10")
        assert len(merged) == 1
        assert merged[0]["merged_by"] == "reviewer"

    def test_pr_merged_different_day(self):
        pr = make_pr(
            created_at="2026-04-08T10:00:00Z",
            merged_at="2026-04-09T15:00:00Z",
            state="closed",
        )
        _, merged, _ = filter_prs_by_date([pr], "2026-04-10")
        assert merged == []

    def test_open_pr_not_stuck_has_reviewer(self):
        pr = make_pr(
            created_at="2026-04-05T10:00:00Z",
            state="open",
            requested_reviewers=[{"login": "reviewer1"}],
        )
        _, _, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert len(open_prs) == 1
        assert open_prs[0]["stuck"] is False

    def test_open_pr_stuck_exact_threshold(self):
        # Created at midnight 3 days before ref date → days_open=3 → stuck
        pr = make_pr(created_at="2026-04-07T00:00:00Z", state="open")
        _, _, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert len(open_prs) == 1
        assert open_prs[0]["days_open"] == 3
        assert open_prs[0]["stuck"] is True

    def test_open_pr_just_under_threshold(self):
        # Created 2 days before ref date at midnight → days_open=2 → NOT stuck
        pr = make_pr(created_at="2026-04-08T00:00:00Z", state="open")
        _, _, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert len(open_prs) == 1
        assert open_prs[0]["days_open"] == 2
        assert open_prs[0]["stuck"] is False

    def test_open_pr_stuck_with_reviewer_not_stuck(self):
        # 5 days open but HAS a reviewer → NOT stuck
        pr = make_pr(
            created_at="2026-04-05T10:00:00Z",
            state="open",
            requested_reviewers=[{"login": "rev"}],
        )
        _, _, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert open_prs[0]["stuck"] is False

    def test_days_open_calculation(self):
        # ref_date is midnight Apr 10; created Apr 3 00:00 → 7 days
        pr = make_pr(created_at="2026-04-03T00:00:00Z", state="open")
        _, _, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert open_prs[0]["days_open"] == 7

    def test_pr_both_opened_and_merged_same_day(self):
        pr = make_pr(
            created_at="2026-04-10T10:00:00Z",
            merged_at="2026-04-10T15:00:00Z",
            state="closed",
            merged_by={"login": "self"},
        )
        opened, merged, _ = filter_prs_by_date([pr], "2026-04-10")
        assert len(opened) == 1
        assert len(merged) == 1

    def test_closed_not_merged_pr(self):
        pr = make_pr(
            created_at="2026-04-08T10:00:00Z",
            state="closed",
            merged_at=None,
        )
        opened, merged, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert merged == []
        assert open_prs == []  # state is "closed", not "open"

    def test_time_to_merge_calculation(self):
        pr = make_pr(
            created_at="2026-04-10T10:00:00Z",
            merged_at="2026-04-10T12:30:00Z",
            state="closed",
        )
        _, merged, _ = filter_prs_by_date([pr], "2026-04-10")
        assert merged[0]["time_to_merge"] == "2.5h"

    def test_labels_extracted(self):
        pr = make_pr(
            state="open",
            labels=[{"name": "bug"}, {"name": "urgent"}],
        )
        _, _, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert open_prs[0]["labels"] == ["bug", "urgent"]

    def test_requested_reviewers_extracted(self):
        pr = make_pr(
            state="open",
            requested_reviewers=[{"login": "rev1"}, {"login": "rev2"}],
        )
        _, _, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert open_prs[0]["requested_reviewers"] == ["rev1", "rev2"]

    def test_missing_user_field(self):
        pr = make_pr(state="open", user={})
        _, _, open_prs = filter_prs_by_date([pr], "2026-04-10")
        assert open_prs[0]["author"] == "unknown"


# ── Issue filtering ──────────────────────────────────────────────────


class TestFilterIssuesByDate:
    def test_empty_list(self):
        opened, closed, open_issues = filter_issues_by_date([], "2026-04-10")
        assert opened == []
        assert closed == []
        assert open_issues == []

    def test_issue_opened_today(self):
        issue = make_issue(created_at="2026-04-10T10:00:00Z")
        opened, _, _ = filter_issues_by_date([issue], "2026-04-10")
        assert len(opened) == 1
        assert opened[0]["number"] == 10

    def test_issue_closed_today(self):
        issue = make_issue(
            created_at="2026-04-08T10:00:00Z",
            closed_at="2026-04-10T15:00:00Z",
            state="closed",
        )
        _, closed, _ = filter_issues_by_date([issue], "2026-04-10")
        assert len(closed) == 1

    def test_open_issue_not_stuck(self):
        # Updated 2 days ago, 0 comments → NOT stuck (under threshold)
        issue = make_issue(
            updated_at="2026-04-08T10:00:00Z",
            comments=0,
        )
        _, _, open_issues = filter_issues_by_date([issue], "2026-04-10")
        assert len(open_issues) == 1
        assert open_issues[0]["stuck"] is False

    def test_open_issue_stuck_exact_threshold(self):
        # Updated at midnight 3 days before ref date → days_since_update=3 → stuck
        issue = make_issue(
            updated_at="2026-04-07T00:00:00Z",
            comments=0,
        )
        _, _, open_issues = filter_issues_by_date([issue], "2026-04-10")
        assert open_issues[0]["days_since_update"] == 3
        assert open_issues[0]["stuck"] is True

    def test_open_issue_stuck_but_has_comments(self):
        # Updated 5 days ago but HAS comments → NOT stuck
        issue = make_issue(
            updated_at="2026-04-05T10:00:00Z",
            comments=1,
        )
        _, _, open_issues = filter_issues_by_date([issue], "2026-04-10")
        assert open_issues[0]["stuck"] is False

    def test_open_issue_days_stale_calculation(self):
        # ref_date is midnight Apr 10; updated Apr 3 00:00 → 7 days
        issue = make_issue(updated_at="2026-04-03T00:00:00Z")
        _, _, open_issues = filter_issues_by_date([issue], "2026-04-10")
        assert open_issues[0]["days_since_update"] == 7

    def test_assignees_extracted(self):
        issue = make_issue(
            assignees=[{"login": "alice"}, {"login": "bob"}],
        )
        _, _, open_issues = filter_issues_by_date([issue], "2026-04-10")
        assert open_issues[0]["assignees"] == ["alice", "bob"]

    def test_issue_missing_updated_at(self):
        issue = make_issue(updated_at="")
        _, _, open_issues = filter_issues_by_date([issue], "2026-04-10")
        # _parse_ts("") returns None → days_stale=0
        assert open_issues[0]["days_since_update"] == 0

    def test_issue_both_opened_and_closed_same_day(self):
        issue = make_issue(
            created_at="2026-04-10T10:00:00Z",
            closed_at="2026-04-10T15:00:00Z",
            state="closed",
        )
        opened, closed, _ = filter_issues_by_date([issue], "2026-04-10")
        assert len(opened) == 1
        assert len(closed) == 1


# ── Workload aggregation ─────────────────────────────────────────────


class TestAggregateWorkload:
    def test_empty_repo_data(self):
        result = aggregate_workload_by_assignee([])
        assert result == []

    def test_in_progress_status(self):
        repo = make_repo_data(
            open_issues=[{"assignees": ["alice"], "days_since_update": 0}],
            commits=[{"author": "alice"}],
        )
        result = aggregate_workload_by_assignee([repo])
        alice = next(r for r in result if r["assignee"] == "alice")
        assert alice["status"] == "In Progress"

    def test_stuck_status(self):
        repo = make_repo_data(
            open_issues=[{"assignees": ["alice"], "days_since_update": 5}],
        )
        result = aggregate_workload_by_assignee([repo])
        alice = next(r for r in result if r["assignee"] == "alice")
        assert alice["status"] == "Stuck"

    def test_backlog_status(self):
        repo = make_repo_data(
            open_issues=[{"assignees": ["alice"], "days_since_update": 1}],
        )
        result = aggregate_workload_by_assignee([repo])
        alice = next(r for r in result if r["assignee"] == "alice")
        assert alice["status"] == "Backlog"

    def test_reviewer_counted(self):
        repo = make_repo_data(
            open_prs=[
                {"author": "bob", "requested_reviewers": ["alice"]},
            ],
        )
        result = aggregate_workload_by_assignee([repo])
        alice = next(r for r in result if r["assignee"] == "alice")
        assert alice["review_requests"] == 1

    def test_multiple_repos_aggregated(self):
        repo1 = make_repo_data(
            open_issues=[{"assignees": ["alice"], "days_since_update": 0}],
            commits=[{"author": "alice"}],
        )
        repo2 = make_repo_data(
            open_issues=[{"assignees": ["alice"], "days_since_update": 0}],
        )
        result = aggregate_workload_by_assignee([repo1, repo2])
        alice = next(r for r in result if r["assignee"] == "alice")
        assert alice["assigned_issues"] == 2

    def test_stuck_threshold_boundary_exact_3(self):
        repo = make_repo_data(
            open_issues=[{"assignees": ["alice"], "days_since_update": 3}],
        )
        result = aggregate_workload_by_assignee([repo])
        alice = next(r for r in result if r["assignee"] == "alice")
        assert alice["status"] == "Stuck"

    def test_stuck_threshold_boundary_2(self):
        repo = make_repo_data(
            open_issues=[{"assignees": ["alice"], "days_since_update": 2}],
        )
        result = aggregate_workload_by_assignee([repo])
        alice = next(r for r in result if r["assignee"] == "alice")
        assert alice["status"] == "Backlog"

    def test_open_prs_authored_counted(self):
        repo = make_repo_data(
            open_prs=[
                {"author": "alice", "requested_reviewers": []},
                {"author": "alice", "requested_reviewers": []},
            ],
        )
        result = aggregate_workload_by_assignee([repo])
        alice = next(r for r in result if r["assignee"] == "alice")
        assert alice["open_prs_authored"] == 2


# ── Label string helper ──────────────────────────────────────────────


class TestLabelStr:
    def test_empty_labels(self):
        assert _label_str([]) == ""

    def test_single_label(self):
        assert _label_str(["bug"]) == "`bug`"

    def test_multiple_labels(self):
        assert _label_str(["bug", "urgent"]) == "`bug` `urgent`"

    def test_none_labels(self):
        assert _label_str(None) == ""


# ── Report generation ────────────────────────────────────────────────


class TestGenerateReport:
    @patch("team_pulse._now_bangkok")
    def test_report_header_contains_date(self, mock_now, tmp_path):
        mock_now.return_value = datetime(2026, 4, 10, 14, 0, tzinfo=timezone.utc)
        report = generate_report("2026-04-10", "am", [make_repo_data()], tmp_path)
        assert "# Daily Pulse — 2026-04-10" in report

    @patch("team_pulse._now_bangkok")
    def test_report_am_period(self, mock_now, tmp_path):
        mock_now.return_value = datetime(2026, 4, 10, 7, 0, tzinfo=timezone.utc)
        report = generate_report("2026-04-10", "am", [make_repo_data()], tmp_path)
        assert "Morning Snapshot" in report

    @patch("team_pulse._now_bangkok")
    def test_report_pm_period(self, mock_now, tmp_path):
        mock_now.return_value = datetime(2026, 4, 10, 18, 0, tzinfo=timezone.utc)
        report = generate_report("2026-04-10", "pm", [make_repo_data()], tmp_path)
        assert "Evening Snapshot" in report

    @patch("team_pulse._now_bangkok")
    def test_empty_repo_data(self, mock_now, tmp_path):
        mock_now.return_value = datetime(2026, 4, 10, 14, 0, tzinfo=timezone.utc)
        report = generate_report("2026-04-10", "am", [make_repo_data()], tmp_path)
        assert "_No commits on this date._" in report
        assert "_No PRs opened on this date._" in report

    @patch("team_pulse._now_bangkok")
    def test_summary_table_counts(self, mock_now, tmp_path):
        mock_now.return_value = datetime(2026, 4, 10, 14, 0, tzinfo=timezone.utc)
        repo = make_repo_data(
            commits=[{"sha": "abc1234", "author": "alice", "message": "fix", "time": "10:00", "hour": 10, "url": ""}],
            prs_opened=[{"number": 1, "title": "PR", "author": "alice", "url": "", "labels": [], "requested_reviewers": []}],
        )
        report = generate_report("2026-04-10", "am", [repo], tmp_path)
        assert "| Commits | 1 |" in report
        assert "| PRs opened | 1 |" in report

    @patch("team_pulse._now_bangkok")
    def test_stuck_alert_section_present(self, mock_now, tmp_path):
        mock_now.return_value = datetime(2026, 4, 10, 14, 0, tzinfo=timezone.utc)
        repo = make_repo_data(
            open_prs=[{
                "number": 42, "title": "Stuck PR", "author": "alice",
                "days_open": 5, "requested_reviewers": [], "labels": [],
                "url": "https://github.com/o/r/pull/42", "stuck": True,
            }],
        )
        report = generate_report("2026-04-10", "am", [repo], tmp_path)
        assert "Stuck Items Alert" in report
        assert "Stuck PRs" in report

    @patch("team_pulse._now_bangkok")
    def test_stuck_alert_section_absent(self, mock_now, tmp_path):
        mock_now.return_value = datetime(2026, 4, 10, 14, 0, tzinfo=timezone.utc)
        report = generate_report("2026-04-10", "am", [make_repo_data()], tmp_path)
        assert "Stuck Items Alert" not in report
