## 1. Implementation
- [ ] 1.1 Implement `read_toml(path: str) -> dict[str, Any] | None` in `stavroslib/parse.py` using `tomllib`
- [ ] 1.2 Handle empty files by returning `None`; propagate `tomllib.TOMLDecodeError` on invalid input
- [ ] 1.3 Add tests `stavroslib/tests/test_parse_toml.py` covering simple, nested, lists, empty, invalid cases
- [ ] 1.4 Run `uv run pytest --cov=stavroslib --cov-report=term-missing` and ensure tests pass
- [ ] 1.5 Type-check with `uv run mypy`

## 2. Review & Approval
- [ ] 2.1 Share proposal for approval (do not implement until approved)

## 3. Post-merge
- [ ] 3.1 Consider updating README with TOML example
