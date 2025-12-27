## 1. Implementation
- [x] 1.1 Implement `read_toml(path: str) -> dict[str, Any] | None` in `stavroslib/parse.py` using `tomllib`
- [x] 1.2 Handle empty files by returning `None`; propagate `tomllib.TOMLDecodeError` on invalid input
- [x] 1.3 Add tests `stavroslib/tests/test_parse_toml.py` covering simple, nested, lists, empty, invalid cases
- [x] 1.4 Run `uv run pytest --cov=stavroslib --cov-report=term-missing` and ensure tests pass
- [x] 1.5 Type-check with `uv run mypy`

## 2. Review & Approval
- [x] 2.1 Share proposal for approval (do not implement until approved)

## 3. Post-merge
- [x] 3.1 Consider updating README with TOML example
