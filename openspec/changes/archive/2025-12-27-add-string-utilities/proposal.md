# Change: Add String Utilities

## Why
Provide common string manipulation and formatting functions to reduce boilerplate. Complements existing `parse.py` module by offering text normalization, transformation, and slug generation patterns commonly needed in data processing pipelines.

## What Changes
- Add `stavroslib/string.py` with functions:
  - `slugify(text: str) -> str` - Convert to URL-safe slugs
  - `truncate(text: str, max_len: int, suffix: str = "...") -> str` - Safely truncate text
  - `capitalize_words(text: str) -> str` - Capitalize each word
  - `remove_accents(text: str) -> str` - Strip diacritics for ASCII compatibility
- Add tests in `stavroslib/tests/test_string.py` covering all functions
- Update README with string utility examples

## Impact
- Affected specs: `string-utilities`
- Affected code: `stavroslib/string.py`, `stavroslib/tests/test_string.py`, `README.md`
- Non-breaking; new module only
- Optional dependency: `unicodedata` (stdlib, no new packages)
