# Change: Add Date/Time Helper Utilities

## Why
The library provides parsing utilities (YAML, TOML) and misc utilities (notifications, API calls) but lacks date/time helpers. Common operations like parsing various date formats, formatting for display, and generating human-readable relative times ("2 hours ago", "in 3 days") are frequently needed across projects.

## What Changes
- Add new `datetime.py` module to `stavroslib/`
- Add `parse_datetime()` function supporting ISO 8601 and common date formats
- Add `format_datetime()` function with preset output formats (ISO, human-readable, short)
- Add `relative_time()` function for past and future relative descriptions
- Add `python-dateutil` as a new dependency for flexible parsing
- Add comprehensive tests for all new functions

## Impact
- Affected specs: Creates new `datetime-utilities` capability
- Affected code: `stavroslib/datetime.py` (new), `stavroslib/__init__.py`, `pyproject.toml`
- Dependencies: Adds `python-dateutil` runtime dependency and `types-python-dateutil` for type checking
