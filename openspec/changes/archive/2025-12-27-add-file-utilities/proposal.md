# Change: Add File Utilities

## Why
Provide common file and path operations to reduce boilerplate code. Complements existing `parse.py` (YAML/TOML) and `pdf.py` modules by offering safe file operations with encoding handling, directory creation, and file discovery patterns.

## What Changes
- Add `stavroslib/file.py` with functions:
  - `ensure_dir(path: str) -> Path` - Create directory if missing
  - `read_file(path: str, encoding: str = "utf-8") -> str` - Read text file
  - `write_file(path: str, content: str, encoding: str = "utf-8") -> None` - Write text file
  - `find_files(pattern: str, root: str = ".") -> list[str]` - Glob-based file finding
- Add tests in `stavroslib/tests/test_file.py` covering all functions
- Update README with file utility examples

## Impact
- Affected specs: `file-utilities`
- Affected code: `stavroslib/file.py`, `stavroslib/tests/test_file.py`, `README.md`
- Non-breaking; new module only
- No new dependencies (uses stdlib `pathlib` and `glob`)
