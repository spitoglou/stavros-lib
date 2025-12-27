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


## Usage

### Read TOML config

```python
from stavroslib.parse import read_toml

config = read_toml("config.toml")
if config is not None:
    db = config["database"]
    print(db["host"], db["port"])  # localhost 5432
```

Notes:
- Returns `None` for empty files.
- Raises `tomllib.TOMLDecodeError` for invalid TOML.

## Install

Install the released version `v0.22` directly from GitHub:

```bash
pip install "git+https://github.com/spitoglou/stavros-lib.git@v0.22" -U
```


pip install git+https://github.com/spitoglou/stavros-lib.git -U