"""Tests for datetime utilities."""

from datetime import datetime, timedelta, timezone

import pytest

from stavroslib.datetime import format_datetime, parse_datetime, relative_time


class TestParseDatetime:
    """Tests for parse_datetime function."""

    def test_parse_iso_8601_with_timezone(self):
        result = parse_datetime("2024-01-15T10:30:00Z")
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 10
        assert result.minute == 30
        assert result.second == 0

    def test_parse_iso_8601_without_timezone(self):
        result = parse_datetime("2024-01-15T10:30:00")
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_parse_date_with_slashes_dmy(self):
        result = parse_datetime("15/01/2024")
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_parse_human_readable_date(self):
        result = parse_datetime("Jan 15, 2024")
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_parse_full_month_name(self):
        result = parse_datetime("January 15, 2024")
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_parse_iso_date_only(self):
        result = parse_datetime("2024-01-15")
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_parse_invalid_date_raises_valueerror(self):
        with pytest.raises(ValueError, match="Cannot parse date string"):
            parse_datetime("not a date")

    def test_parse_empty_string_raises_valueerror(self):
        with pytest.raises(ValueError, match="Cannot parse date string"):
            parse_datetime("")


class TestFormatDatetime:
    """Tests for format_datetime function."""

    def test_format_iso(self):
        dt = datetime(2024, 1, 15, 10, 30, 0)
        result = format_datetime(dt, preset="iso")
        assert result == "2024-01-15T10:30:00"

    def test_format_human(self):
        dt = datetime(2024, 1, 15, 10, 30, 0)
        result = format_datetime(dt, preset="human")
        assert result == "January 15, 2024"

    def test_format_human_single_digit_day(self):
        dt = datetime(2024, 1, 5, 10, 30, 0)
        result = format_datetime(dt, preset="human")
        assert result == "January 5, 2024"

    def test_format_short(self):
        dt = datetime(2024, 1, 15, 10, 30, 0)
        result = format_datetime(dt, preset="short")
        assert result == "01/15/24"

    def test_format_default_is_iso(self):
        dt = datetime(2024, 1, 15, 10, 30, 0)
        result = format_datetime(dt)
        assert result == "2024-01-15T10:30:00"

    def test_format_invalid_preset_raises_valueerror(self):
        dt = datetime(2024, 1, 15)
        with pytest.raises(ValueError, match="Unknown preset"):
            format_datetime(dt, preset="unknown")  # type: ignore[arg-type]


class TestRelativeTime:
    """Tests for relative_time function."""

    def test_just_now_past(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 15, 11, 59, 30)  # 30 seconds ago
        result = relative_time(dt, now=now)
        assert result == "just now"

    def test_just_now_future(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 15, 12, 0, 30)  # 30 seconds in future
        result = relative_time(dt, now=now)
        assert result == "just now"

    def test_minutes_ago(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 15, 11, 55, 0)  # 5 minutes ago
        result = relative_time(dt, now=now)
        assert result == "5 minutes ago"

    def test_one_minute_ago(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 15, 11, 59, 0)  # 1 minute ago
        result = relative_time(dt, now=now)
        assert result == "1 minute ago"

    def test_in_minutes(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 15, 12, 5, 0)  # 5 minutes in future
        result = relative_time(dt, now=now)
        assert result == "in 5 minutes"

    def test_hours_ago(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 15, 10, 0, 0)  # 2 hours ago
        result = relative_time(dt, now=now)
        assert result == "2 hours ago"

    def test_one_hour_ago(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 15, 11, 0, 0)  # 1 hour ago
        result = relative_time(dt, now=now)
        assert result == "1 hour ago"

    def test_in_hours(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 15, 14, 0, 0)  # 2 hours in future
        result = relative_time(dt, now=now)
        assert result == "in 2 hours"

    def test_days_ago(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 12, 12, 0, 0)  # 3 days ago
        result = relative_time(dt, now=now)
        assert result == "3 days ago"

    def test_one_day_ago(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 14, 12, 0, 0)  # 1 day ago
        result = relative_time(dt, now=now)
        assert result == "1 day ago"

    def test_in_days(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 1, 18, 12, 0, 0)  # 3 days in future
        result = relative_time(dt, now=now)
        assert result == "in 3 days"

    def test_months_ago(self):
        now = datetime(2024, 6, 15, 12, 0, 0)
        dt = datetime(2024, 4, 15, 12, 0, 0)  # ~2 months ago
        result = relative_time(dt, now=now)
        assert result == "2 months ago"

    def test_in_months(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2024, 4, 15, 12, 0, 0)  # ~3 months in future
        result = relative_time(dt, now=now)
        assert result == "in 3 months"

    def test_years_ago(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2022, 1, 15, 12, 0, 0)  # 2 years ago
        result = relative_time(dt, now=now)
        assert result == "2 years ago"

    def test_in_years(self):
        now = datetime(2024, 1, 15, 12, 0, 0)
        dt = datetime(2026, 1, 15, 12, 0, 0)  # 2 years in future
        result = relative_time(dt, now=now)
        assert result == "in 2 years"

    def test_timezone_aware_datetime(self):
        now = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        dt = datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc)  # 2 hours ago
        result = relative_time(dt, now=now)
        assert result == "2 hours ago"

    def test_mixed_timezone_awareness(self):
        now = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        dt = datetime(2024, 1, 15, 10, 0, 0)  # naive, 2 hours ago
        result = relative_time(dt, now=now)
        assert result == "2 hours ago"
