# toml-parsing Specification

## Purpose
Provide a built-in, dependency-free way to read TOML configuration files using Python 3.13's stdlib `tomllib`.

## Requirements

### Requirement: TOML Parsing
The library SHALL provide a TOML parsing function `read_toml(path: str) -> dict[str, Any] | None` implemented using Python's stdlib `tomllib`.

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
