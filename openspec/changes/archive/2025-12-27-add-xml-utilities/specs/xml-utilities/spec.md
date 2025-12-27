# xml-utilities Specification

## Purpose
Provide utilities for parsing XML documents to Python dictionaries and removing namespaces, complementing existing config parsing capabilities.

## ADDED Requirements

### Requirement: XML to Dictionary Conversion
The library SHALL provide an `xml_to_dict()` function that parses XML strings into nested Python dictionaries. Element attributes SHALL be prefixed with `@`, text content SHALL use `#text` key when mixed with children/attributes.

#### Scenario: Parse simple XML
- **WHEN** `xml_to_dict("<root><item>value</item></root>")` is called
- **THEN** a dict `{"root": {"item": "value"}}` is returned

#### Scenario: Parse XML with attributes
- **WHEN** XML with attributes like `<root id="123"><item>value</item></root>` is parsed
- **THEN** attributes are prefixed with `@`: `{"root": {"@id": "123", "item": "value"}}`

#### Scenario: Parse nested XML
- **WHEN** XML with nested elements is parsed
- **THEN** nested dicts are returned preserving structure

#### Scenario: Parse XML with repeated elements
- **WHEN** XML has multiple elements with same tag like `<items><item>1</item><item>2</item></items>`
- **THEN** repeated elements become a list: `{"items": {"item": ["1", "2"]}}`

#### Scenario: Invalid XML
- **WHEN** malformed XML is provided
- **THEN** an appropriate exception is raised (XMLSyntaxError or similar)

### Requirement: Remove XML Namespaces
The library SHALL provide a `remove_namespace()` function that strips namespaces from XML documents using XSLT transformation.

#### Scenario: Remove simple namespace
- **WHEN** `remove_namespace('<root xmlns="http://example.com"><item>value</item></root>')` is called
- **THEN** namespace-free XML `<root><item>value</item></root>` is returned

#### Scenario: Remove multiple namespaces
- **WHEN** XML with multiple namespace declarations is provided
- **THEN** all namespaces are stripped, preserving element structure

#### Scenario: Preserve element content
- **WHEN** namespaced XML is processed
- **THEN** element text, attributes, and structure are preserved (only namespaces removed)

#### Scenario: Handle no namespaces
- **WHEN** XML without namespaces is provided
- **THEN** XML is returned unchanged
