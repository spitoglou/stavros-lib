# Change: Add Environment Variable Loading

## Why
Provide simple `.env` file parsing to complement existing YAML/TOML config loading. Environment files are ubiquitous in modern development, and having built-in support reduces the need for external dependencies like python-dotenv.

## What Changes
- Enhance `stavroslib/parse.py` with:
  - `read_env(file_path: str) -> dict[str, str]` - Parse `.env` file to dict
  - Support standard `.env` format (KEY=VALUE, comments with #, quoted values)
  - Handle multiline values, empty lines, and whitespace
- Add tests in `stavroslib/tests/test_parse.py` covering .env parsing edge cases
- Update README with .env loading examples

## Impact
- Affected specs: `env-loading`
- Affected code: `stavroslib/parse.py`, `stavroslib/tests/test_parse.py`, `README.md`
- Non-breaking; adds function to existing module
- No new dependencies (uses stdlib only)
