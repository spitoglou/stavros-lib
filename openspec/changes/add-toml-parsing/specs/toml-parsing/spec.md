## ADDED Requirements

### Requirement: TOML Parsing
The library SHALL provide a TOML parsing function `read_toml(path: str) -> dict[str, Any] | None` implemented using Python's stdlib `tomllib`.

- It SHALL return a mapping structure for valid TOML documents.
- It SHALL return `None` for empty files.
- It SHALL raise `tomllib.TOMLDecodeError` for invalid TOML content.
- It SHALL not introduce new external dependencies.

#### Scenario: Parse simple TOML
- **WHEN** a file with simple key-value TOML is provided
- **THEN** `read_toml(path)` returns a dict with those keys and values

#### Scenario: Parse nested TOML
- **WHEN** a file with nested tables is provided
- **THEN** `read_toml(path)` returns nested dicts corresponding to the tables

#### Scenario: Parse list values
- **WHEN** a file contains list/array values
- **THEN** `read_toml(path)` returns Python lists for those arrays

#### Scenario: Empty file returns None
- **WHEN** an empty file is provided
- **THEN** `read_toml(path)` returns `None`

#### Scenario: Invalid TOML raises
- **WHEN** a file contains invalid TOML syntax
- **THEN** `read_toml(path)` raises `tomllib.TOMLDecodeError`
