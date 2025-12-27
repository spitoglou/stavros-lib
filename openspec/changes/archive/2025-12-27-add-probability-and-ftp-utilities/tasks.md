# Implementation Tasks

## 1. Implementation
- [x] Create `stavroslib/probability.py` with odds conversion functions
- [x] Create `stavroslib/probability.py` with binomial probability functions
- [x] Create `stavroslib/ftp.py` with FTP upload functions
- [x] Create `stavroslib/ftp.py` with FTP monitoring functions
- [x] Create `stavroslib/ftp.py` with FtpHelper class for directory operations
- [x] Update `stavroslib/__init__.py` to export new functions

## 2. Testing
- [x] Create `stavroslib/tests/test_probability.py` with odds conversion tests
- [x] Add binomial probability calculation tests
- [x] Create `stavroslib/tests/test_ftp.py` with mocked FTP tests
- [x] Add FTP monitoring and directory tests
- [x] Run `uv run pytest` to verify all tests pass
- [x] Run `uv run pytest --cov=stavroslib` to check coverage

## 3. Documentation
- [x] Add docstrings to all probability functions
- [x] Add docstrings to all FTP functions
- [x] Add type hints to all functions

## 4. Validation
- [x] Run `openspec validate add-probability-and-ftp-utilities --strict`
- [x] Fix any validation issues
- [x] Verify tests pass with `uv run pytest`
