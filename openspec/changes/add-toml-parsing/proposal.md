# Change: Add TOML Parsing Utility

## Why
Provide a built-in, dependency-free way to read TOML configuration files, complementing existing YAML parsing. Python 3.13 includes `tomllib`, so this adds capability without increasing dependencies.

## What Changes
- Add `read_toml(path: str) -> dict[str, Any] | None` implemented via stdlib `tomllib`
- Return `None` for empty files; propagate `tomllib.TOMLDecodeError` for invalid content
- Place implementation in `stavroslib/parse.py` alongside `read_yaml`
- Add tests `stavroslib/tests/test_parse_toml.py` covering success, nested, lists, empty, invalid cases
- No new dependencies; keep library minimal

## Impact
- Affected specs: `toml-parsing`
- Affected code: `stavroslib/parse.py`, `stavroslib/tests/test_parse_toml.py`
- Non-breaking; new function only
