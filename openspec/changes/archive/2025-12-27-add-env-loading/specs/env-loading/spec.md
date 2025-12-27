# env-loading Specification

## Purpose
Provide simple environment variable file (.env) parsing to complement YAML/TOML configuration loading.

## ADDED Requirements

### Requirement: Environment File Parsing
The library SHALL provide a `read_env()` function that parses `.env` files into Python dictionaries with string keys and values.

#### Scenario: Parse simple key-value pairs
- **WHEN** `read_env(".env")` is called on a file with `KEY=value`
- **THEN** a dict `{"KEY": "value"}` is returned

#### Scenario: Handle comments
- **WHEN** a line starts with `#` (comment)
- **THEN** the line is ignored

#### Scenario: Handle inline comments
- **WHEN** a line contains `KEY=value # comment`
- **THEN** only `{"KEY": "value"}` is parsed (comment stripped)

#### Scenario: Handle quoted values
- **WHEN** a line contains `KEY="value with spaces"`
- **THEN** `{"KEY": "value with spaces"}` is returned (quotes stripped)

#### Scenario: Handle single quotes
- **WHEN** a line contains `KEY='value'`
- **THEN** `{"KEY": "value"}` is returned

#### Scenario: Handle empty values
- **WHEN** a line contains `KEY=` (empty value)
- **THEN** `{"KEY": ""}` is returned

#### Scenario: Skip empty lines
- **WHEN** the file contains blank lines
- **THEN** blank lines are ignored

#### Scenario: Handle whitespace
- **WHEN** a line has extra whitespace like `  KEY = value  `
- **THEN** whitespace is trimmed: `{"KEY": "value"}`

#### Scenario: Handle export syntax
- **WHEN** a line contains `export KEY=value`
- **THEN** `{"KEY": "value"}` is returned (export prefix ignored)

#### Scenario: File not found
- **WHEN** `read_env("nonexistent.env")` is called
- **THEN** a `FileNotFoundError` is raised

#### Scenario: Return empty dict for empty file
- **WHEN** an empty `.env` file is provided
- **THEN** an empty dict `{}` is returned
