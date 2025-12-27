# Change: Add XML Utilities

## Why
Provide XML parsing and manipulation utilities to complement existing config parsing (YAML/TOML). Converting XML to dictionaries is a common need for API integrations and data processing, and removing namespaces simplifies working with complex XML documents.

## What Changes
- Add `stavroslib/xml.py` with functions:
  - `xml_to_dict(xml_string: str) -> dict[str, Any]` - Parse XML string to nested dict
  - `remove_namespace(xml_string: str) -> str` - Strip XML namespaces using XSLT
- Add dependency `lxml` for robust XML parsing (widely used, minimal)
- Add tests in `stavroslib/tests/test_xml.py` covering both functions with various XML structures
- Update README with XML utility examples

## Impact
- Affected specs: `xml-utilities`
- Affected code: `stavroslib/xml.py`, `stavroslib/tests/test_xml.py`, `README.md`, `pyproject.toml`
- Non-breaking; new module only
- New dependency: `lxml` (industry standard for XML in Python)
