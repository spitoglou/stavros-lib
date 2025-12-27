## 1. Implementation
- [x] 1.1 Implement `read_env(file_path: str) -> dict[str, str]` in `stavroslib/parse.py`
- [x] 1.2 Support KEY=VALUE syntax, comments (#), quoted values, multiline values
- [x] 1.3 Add tests in `stavroslib/tests/test_parse.py` covering simple, comments, quotes, multiline, empty
- [x] 1.4 Run `uv run pytest --cov=stavroslib --cov-report=term-missing` and ensure tests pass
- [x] 1.5 Type-check with `uv run mypy`

## 2. Review & Approval
- [x] 2.1 Share proposal for approval (do not implement until approved)

## 3. Post-merge
- [x] 3.1 Update README with .env loading example
