# Change: Add Probability and FTP Utilities

## Why
The library needs statistical/probability functions for odds conversion and binomial calculations, plus FTP upload capabilities for remote file management. These utilities exist in the soccer project and are generic enough for reuse.

## What Changes
- Add `stavroslib.probability` module with odds conversion and binomial probability functions
- Add `stavroslib.ftp` module with FTP upload, monitoring, and directory management
- Add comprehensive tests for both modules
- Update package exports in `__init__.py`

## Impact
- Affected specs: New capabilities `probability-utilities` and `ftp-utilities`
- Affected code: New files `stavroslib/probability.py`, `stavroslib/ftp.py`, test files, and `__init__.py`
- Dependencies: No new dependencies (uses stdlib `ftplib` and `math`)
