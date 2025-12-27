# stavros-lib

This project uses [UV](https://github.com/astral-sh/uv) for dependency management. UV is a fast and efficient package manager for Python.

## Setup

1. Install UV:
   ```bash
   pip install uv
   ```

2. Create a virtual environment:
   ```bash
   uv venv
   ```

3. Install dependencies:
   ```bash
   uv pip install -e .
   ```

4. Run tests:
   ```bash
   uv run pytest
   ```



pip install git+https://github.com/spitoglou/stavros-lib.git -U