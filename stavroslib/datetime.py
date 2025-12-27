"""Date/Time Helper Utilities"""

from datetime import datetime, timezone
from typing import Literal

from dateutil import parser as dateutil_parser
from dateutil.parser import ParserError


def parse_datetime(date_string: str) -> datetime:
    """Parse a date/time string into a datetime object.

    Supports ISO 8601 format and common date formats like "15/01/2024",
    "Jan 15, 2024", "2024-01-15".

    Arguments:
        date_string: The date/time string to parse.

    Returns:
        A datetime object representing the parsed date/time.

    Raises:
        ValueError: If the string cannot be parsed as a valid date/time.
    """
    try:
        return dateutil_parser.parse(date_string)
    except ParserError as e:
        raise ValueError(f"Cannot parse date string: {date_string}") from e


FormatPreset = Literal["iso", "human", "short"]


def format_datetime(dt: datetime, preset: FormatPreset = "iso") -> str:
    """Format a datetime object using a preset format.

    Arguments:
        dt: The datetime object to format.
        preset: The format preset to use. One of:
            - "iso": ISO 8601 format (e.g., "2024-01-15T10:30:00")
            - "human": Human-readable format (e.g., "January 15, 2024")
            - "short": Short format (e.g., "01/15/24")

    Returns:
        A formatted date/time string.

    Raises:
        ValueError: If an unknown preset is specified.
    """
    if preset == "iso":
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    elif preset == "human":
        return dt.strftime("%B %d, %Y").replace(" 0", " ")
    elif preset == "short":
        return dt.strftime("%m/%d/%y")
    else:
        raise ValueError(f"Unknown preset: {preset}")


def relative_time(dt: datetime, now: datetime | None = None) -> str:
    """Get a human-readable relative time description.

    Arguments:
        dt: The datetime to describe relative to now.
        now: Optional reference time (defaults to current UTC time).

    Returns:
        A human-readable string like "2 hours ago", "in 3 days", or "just now".
    """
    if now is None:
        now = datetime.now(timezone.utc)

    # Make both datetimes offset-aware or offset-naive for comparison
    if dt.tzinfo is None and now.tzinfo is not None:
        now = now.replace(tzinfo=None)
    elif dt.tzinfo is not None and now.tzinfo is None:
        dt = dt.replace(tzinfo=None)

    diff = dt - now
    total_seconds = diff.total_seconds()
    is_future = total_seconds > 0
    abs_seconds = abs(total_seconds)

    # Just now (within 60 seconds)
    if abs_seconds < 60:
        return "just now"

    # Minutes
    if abs_seconds < 3600:
        minutes = int(abs_seconds // 60)
        unit = "minute" if minutes == 1 else "minutes"
        return f"in {minutes} {unit}" if is_future else f"{minutes} {unit} ago"

    # Hours
    if abs_seconds < 86400:
        hours = int(abs_seconds // 3600)
        unit = "hour" if hours == 1 else "hours"
        return f"in {hours} {unit}" if is_future else f"{hours} {unit} ago"

    # Days
    if abs_seconds < 2592000:  # ~30 days
        days = int(abs_seconds // 86400)
        unit = "day" if days == 1 else "days"
        return f"in {days} {unit}" if is_future else f"{days} {unit} ago"

    # Months
    if abs_seconds < 31536000:  # ~365 days
        months = int(abs_seconds // 2592000)
        unit = "month" if months == 1 else "months"
        return f"in {months} {unit}" if is_future else f"{months} {unit} ago"

    # Years
    years = int(abs_seconds // 31536000)
    unit = "year" if years == 1 else "years"
    return f"in {years} {unit}" if is_future else f"{years} {unit} ago"
