## 1. Implementation
- [x] 1.1 Add `lxml` dependency to `pyproject.toml`
- [x] 1.2 Implement `xml_to_dict(xml_string: str) -> dict[str, Any]` in `stavroslib/xml.py`
- [x] 1.3 Implement `remove_namespace(xml_string: str) -> str`
- [x] 1.4 Add tests in `stavroslib/tests/test_xml.py` covering simple, nested, attributes, namespaced XML
- [x] 1.5 Run `uv run pytest --cov=stavroslib --cov-report=term-missing` and ensure tests pass
- [x] 1.6 Type-check with `uv run mypy`

## 2. Review & Approval
- [x] 2.1 Share proposal for approval (do not implement until approved)

## 3. Post-merge
- [x] 3.1 Update README with XML utility examples
