## Purpose
This specification outlines the requirements for using UV as the package manager for the `stavros-lib` project.

## Requirements

### Requirement: UV Package Manager
The project SHALL use UV as the primary package manager for installing and managing dependencies.

#### Scenario: Install Dependencies
- **WHEN** a developer runs `uv sync`
- **THEN** all dependencies from `uv.lock` are installed in the virtual environment.

#### Scenario: Create Virtual Environment
- **WHEN** a developer runs `uv venv`
- **THEN** a new virtual environment is created in the project directory.

#### Scenario: Lock Dependencies
- **WHEN** a developer runs `uv lock`
- **THEN** a lock file is generated to ensure deterministic dependency resolution.

#### Scenario: Run Tests
- **WHEN** a developer runs `uv run pytest`
- **THEN** all tests are executed successfully.

### Requirement: Dependency Installation
The project SHALL use UV instead of `pip` for installing dependencies.

#### Scenario: Install Dependencies in CI/CD
- **WHEN** the CI/CD pipeline runs `uv sync`
- **THEN** all dependencies are installed successfully, and the pipeline proceeds without errors.

#### Scenario: Add Dependencies
- **WHEN** a developer runs `uv add <package>`
- **THEN** the package is added to `pyproject.toml` and the lock file is updated.

#### Scenario: Update Dependencies
- **WHEN** a developer updates a dependency in `pyproject.toml`
- **THEN** running `uv lock` regenerates the lock file to reflect the changes.
