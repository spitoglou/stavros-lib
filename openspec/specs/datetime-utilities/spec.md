# datetime-utilities Specification

## Purpose
TBD - created by archiving change add-datetime-helpers. Update Purpose after archive.
## Requirements
### Requirement: Date/Time Parsing
The library SHALL provide a `parse_datetime()` function that accepts a date/time string and returns a Python `datetime` object. The function SHALL support ISO 8601 format and common date formats (e.g., "15/01/2024", "Jan 15, 2024", "2024-01-15").

#### Scenario: Parse ISO 8601 format
- **WHEN** `parse_datetime("2024-01-15T10:30:00Z")` is called
- **THEN** a datetime object representing January 15, 2024 at 10:30:00 UTC is returned

#### Scenario: Parse common date format with slashes
- **WHEN** `parse_datetime("15/01/2024")` is called
- **THEN** a datetime object representing January 15, 2024 is returned

#### Scenario: Parse human-readable date
- **WHEN** `parse_datetime("Jan 15, 2024")` is called
- **THEN** a datetime object representing January 15, 2024 is returned

#### Scenario: Invalid date string
- **WHEN** `parse_datetime("not a date")` is called
- **THEN** a `ValueError` is raised

### Requirement: Date/Time Formatting
The library SHALL provide a `format_datetime()` function that accepts a datetime object and a preset name, returning a formatted string. Supported presets SHALL include "iso" (ISO 8601), "human" (e.g., "January 15, 2024"), and "short" (e.g., "01/15/24").

#### Scenario: Format as ISO 8601
- **WHEN** `format_datetime(dt, preset="iso")` is called with a datetime
- **THEN** a string in ISO 8601 format is returned (e.g., "2024-01-15T10:30:00")

#### Scenario: Format as human-readable
- **WHEN** `format_datetime(dt, preset="human")` is called with a datetime
- **THEN** a string like "January 15, 2024" is returned

#### Scenario: Format as short
- **WHEN** `format_datetime(dt, preset="short")` is called with a datetime
- **THEN** a string like "01/15/24" is returned

#### Scenario: Invalid preset
- **WHEN** `format_datetime(dt, preset="unknown")` is called
- **THEN** a `ValueError` is raised

### Requirement: Relative Time Description
The library SHALL provide a `relative_time()` function that accepts a datetime and returns a human-readable string describing the time relative to now. The function SHALL support both past times ("2 hours ago", "3 days ago") and future times ("in 2 hours", "in 3 days").

#### Scenario: Time in recent past
- **WHEN** `relative_time(dt)` is called with a datetime 2 hours before now
- **THEN** "2 hours ago" is returned

#### Scenario: Time in past days
- **WHEN** `relative_time(dt)` is called with a datetime 3 days before now
- **THEN** "3 days ago" is returned

#### Scenario: Time in near future
- **WHEN** `relative_time(dt)` is called with a datetime 2 hours after now
- **THEN** "in 2 hours" is returned

#### Scenario: Time in future days
- **WHEN** `relative_time(dt)` is called with a datetime 3 days after now
- **THEN** "in 3 days" is returned

#### Scenario: Just now
- **WHEN** `relative_time(dt)` is called with a datetime within the last minute
- **THEN** "just now" is returned

