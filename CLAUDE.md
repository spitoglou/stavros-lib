<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

---

# stavros-lib: Python Utility Library

## Overview
A lightweight Python 3.13 utility library providing modular, well-tested functionality for common programming tasks. Uses UV for dependency management, maintains 98%+ test coverage, and follows spec-driven development with OpenSpec.

## Current Modules

| Module | Purpose | Functions | Coverage |
|--------|---------|-----------|----------|
| `datetime.py` | Date/time utilities | parse_datetime, format_datetime, relative_time | 96% |
| `dict.py` | Dictionary operations | merge_dicts | 100% |
| `file.py` | File & path operations | ensure_dir, read_file, write_file, find_files | 100% |
| `misc.py` | Miscellaneous utilities | get_country_data, sys_not | 80% |
| `parse.py` | Config parsing | read_yaml, read_toml, read_env | 97% |
| `pdf.py` | PDF generation | register_pdf_fonts, style helpers | 74% |
| `string.py` | String manipulation | slugify, truncate, capitalize_words, remove_accents | 100% |
| `xml.py` | XML parsing | xml_to_dict, remove_namespace | 95% |

## Architecture Principles

1. **Modular Design**: Each module focuses on a specific domain
2. **Minimal Dependencies**: Uses stdlib where possible; external deps include requests, PyYAML, plyer, reportlab, lxml
3. **Type-Safe**: All code is fully typed; validated with mypy
4. **Well-Tested**: Comprehensive pytest suites; 98% overall coverage
5. **Documented**: Docstrings, README examples, and formal specs (OpenSpec)
6. **Spec-Driven**: Changes follow OpenSpec proposal → implementation → archive workflow

## Testing & Quality
- **Framework**: pytest with pytest-cov
- **Coverage Target**: 98%+ (currently 98%)
- **Type Checking**: mypy (zero errors)
- **Dependency Management**: UV with deterministic lock file

## Development Workflow
1. Read OpenSpec specs in `openspec/specs/`
2. Propose changes in `openspec/changes/` with delta specs
3. Implement with tests (maintain coverage)
4. Validate with `openspec validate --strict`
5. Archive completed changes to `openspec/changes/archive/`

## Key Files
- `pyproject.toml` - Package config, dependencies, dev extras
- `openspec/project.md` - Project context & conventions
- `openspec/specs/` - 7 validated specs for all implemented capabilities
- `openspec/changes/archive/` - Completed change proposals
