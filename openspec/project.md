# Project Context

## Purpose
The `stavros-lib` project is a Python library designed to provide common utilities and reusable components for various tasks. It includes functionalities for dictionary operations, miscellaneous utilities (e.g., fetching country data, system notifications), YAML parsing, and PDF generation. The library is intended to simplify and standardize common operations across different projects.

## Tech Stack
- **Programming Language**: Python
- **Package Manager**: UV (for dependency management and virtual environments).
- **Libraries and Frameworks**:
  - `requests`: For making HTTP requests (e.g., fetching country data).
  - `loguru`: For logging.
  - `plyer`: For generating system notifications.
  - `PyYAML`: For YAML parsing.
  - `reportlab`: For PDF generation.
- **Testing**: `pytest` for unit testing.
- **Code Quality**: `flake8`, `autopep8`, and `pycodestyle` for linting and formatting.

## Project Conventions

### Code Style
- The project follows Python best practices and uses tools like `autopep8` and `flake8` for code formatting and linting.
- Functions and variables use snake_case naming conventions.
- Docstrings are provided for functions to explain their purpose, arguments, and return values.

### Architecture Patterns
- The library is modular, with functionalities split into separate files (e.g., `dict.py`, `misc.py`, `parse.py`, `pdf.py`).
- Each module focuses on a specific domain (e.g., dictionary operations, miscellaneous utilities).

### Testing Strategy
- Unit tests are written using `pytest` and are located in the `stavroslib/tests` directory.
- Tests are minimal but cover core functionalities (e.g., dictionary merging, fetching country data).

### Git Workflow
- The project uses a simple Git workflow with a `main` branch.
- No explicit branching strategy is documented, but contributions are likely made directly to the `main` branch.

### Dependency Management
- The project uses UV for dependency management and virtual environment creation.
- Dependencies are defined in `pyproject.toml` with flexible versioning.
- A lock file (`uv.lock`) is used to ensure deterministic dependency resolution.

## Domain Context
- The library is designed for general-purpose use, with a focus on simplifying common tasks like data manipulation, notifications, and PDF generation.
- It is particularly useful for projects requiring reusable utilities in Python.

## Important Constraints
- The library is lightweight and does not include heavy dependencies like `numpy` or `matplotlib` (commented out in `setup.py`).
- It relies on external APIs (e.g., `restcountries.com`) for fetching country data, which may have rate limits or availability issues.

## External Dependencies
- **RestCountries API**: Used for fetching country data in the `get_country_data` function.
- **ReportLab**: For PDF generation and font management.
- **Plyer**: For cross-platform system notifications.