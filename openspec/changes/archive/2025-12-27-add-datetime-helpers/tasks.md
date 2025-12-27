## 1. Setup
- [x] 1.1 Add `python-dateutil` to dependencies in `pyproject.toml`
- [x] 1.2 Add `types-python-dateutil` to dev dependencies
- [x] 1.3 Run `uv sync` to update lock file

## 2. Implementation
- [x] 2.1 Create `stavroslib/datetime.py` with type annotations
- [x] 2.2 Implement `parse_datetime()` with support for ISO 8601 and common formats
- [x] 2.3 Implement `format_datetime()` with ISO, human-readable, and short presets
- [x] 2.4 Implement `relative_time()` for past ("2 hours ago") and future ("in 3 days")
- [x] 2.5 Export new functions from `stavroslib/__init__.py`

## 3. Testing
- [x] 3.1 Create `stavroslib/tests/test_datetime.py`
- [x] 3.2 Add tests for `parse_datetime()` with various input formats
- [x] 3.3 Add tests for `format_datetime()` preset outputs
- [x] 3.4 Add tests for `relative_time()` past and future cases
- [x] 3.5 Add edge case tests (invalid input, timezone handling)

## 4. Validation
- [x] 4.1 Run type checker (`basedpyright`)
- [x] 4.2 Run test suite (`pytest`)
- [x] 4.3 Update README with usage examples
