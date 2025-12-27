## 1. Implementation
- [x] 1.1 Implement `ensure_dir(path: str) -> Path` in `stavroslib/file.py`
- [x] 1.2 Implement `read_file(path: str, encoding: str = "utf-8") -> str`
- [x] 1.3 Implement `write_file(path: str, content: str, encoding: str = "utf-8") -> None`
- [x] 1.4 Implement `find_files(pattern: str, root: str = ".") -> list[str]`
- [x] 1.5 Add tests in `stavroslib/tests/test_file.py` covering all functions
- [x] 1.6 Run `uv run pytest --cov=stavroslib --cov-report=term-missing` and ensure tests pass
- [x] 1.7 Type-check with `uv run mypy`

## 2. Review & Approval
- [x] 2.1 Share proposal for approval (do not implement until approved)

## 3. Post-merge
- [x] 3.1 Update README with file utility examples
