# string-utilities Specification

## Purpose
Provide common string manipulation functions (slugification, truncation, capitalization, accent removal) to complement existing parsing and text processing modules.

## Requirements

### Requirement: Slugify String
The library SHALL provide a `slugify()` function that converts text to a URL-safe slug. The function SHALL convert to lowercase, replace spaces/special characters with hyphens, and remove accents.

#### Scenario: Simple text conversion
- **WHEN** `slugify("Hello World")` is called
- **THEN** the string "hello-world" is returned

#### Scenario: With special characters
- **WHEN** `slugify("Hello, World!")` is called
- **THEN** the string "hello-world" is returned (punctuation removed)

#### Scenario: With accents
- **WHEN** `slugify("Café au Lait")` is called
- **THEN** the string "cafe-au-lait" is returned (accents removed)

#### Scenario: Multiple spaces
- **WHEN** `slugify("Hello    World")` is called
- **THEN** the string "hello-world" is returned (multiple spaces collapsed)

### Requirement: Truncate Text
The library SHALL provide a `truncate()` function that safely truncates text to a maximum length, appending a suffix (default: "...") if truncated.

#### Scenario: Text within limit
- **WHEN** `truncate("Hello", max_len=10)` is called with text shorter than max_len
- **THEN** the original text "Hello" is returned

#### Scenario: Text exceeds limit
- **WHEN** `truncate("Hello World", max_len=8)` is called with text exceeding max_len
- **THEN** a truncated string "Hello..." is returned (8 characters total with suffix)

#### Scenario: Custom suffix
- **WHEN** `truncate("Hello World", max_len=8, suffix="…")` is called with custom suffix
- **THEN** a string with custom suffix is returned

#### Scenario: Zero max_len
- **WHEN** `truncate("Hello", max_len=0)` is called
- **THEN** an empty string or appropriate behavior is returned

### Requirement: Capitalize Words
The library SHALL provide a `capitalize_words()` function that capitalizes the first letter of each word while lowercasing the rest.

#### Scenario: Simple text
- **WHEN** `capitalize_words("hello world")` is called
- **THEN** the string "Hello World" is returned

#### Scenario: Mixed case
- **WHEN** `capitalize_words("heLLo WoRLd")` is called
- **THEN** the string "Hello World" is returned

#### Scenario: With special characters
- **WHEN** `capitalize_words("hello-world test")` is called
- **THEN** the string "Hello-World Test" is returned (hyphens don't split words)

#### Scenario: Empty string
- **WHEN** `capitalize_words("")` is called
- **THEN** an empty string is returned

### Requirement: Remove Accents
The library SHALL provide a `remove_accents()` function that strips diacritical marks (accents) from Unicode characters, converting them to ASCII equivalents.

#### Scenario: French accents
- **WHEN** `remove_accents("Café Naïve Résumé")` is called
- **THEN** the string "Cafe Naive Resume" is returned

#### Scenario: Spanish accents
- **WHEN** `remove_accents("Niño Español")` is called
- **THEN** the string "Nino Espanol" is returned

#### Scenario: No accents
- **WHEN** `remove_accents("Hello World")` is called
- **THEN** the original string "Hello World" is returned (unchanged)

#### Scenario: Mixed accents
- **WHEN** `remove_accents("Ångström café")` is called
- **THEN** the string "Angstrom cafe" is returned
