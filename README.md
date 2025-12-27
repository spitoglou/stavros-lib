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

### Read YAML config

```python
from stavroslib.parse import read_yaml

config = read_yaml("config.yaml")
if config:
   print(config.get("name"))
```

### Merge dictionaries

```python
from stavroslib.dict import merge_dicts

d1 = {"name": "Stavros"}
d2 = {"last": "Pitoglou"}
merged = merge_dicts(d1, d2)
# {"name": "Stavros", "last": "Pitoglou"}
```

### Country data (RestCountries)

```python
from stavroslib.misc import get_country_data

data = get_country_data("Greece")
print(data[0]["name"])  # "Greece"
```

Note: Calls the public RestCountries API; requires internet and may be rate-limited. Prefer stubs/mocks in tests.

### System notification (plyer)

```python
from stavroslib.misc import sys_not

sys_not(title="Hello", message="This is a system notification", timeout=5)
```

Note: May no-op in headless environments or where OS notifications are disabled.

### PDF fonts and styles (ReportLab)

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from stavroslib.pdf import register_pdf_fonts, heading_1, arial_11_justified

register_pdf_fonts()  # requires font files under fonts/

doc = SimpleDocTemplate("example.pdf", pagesize=A4)
story = []
story.append(Paragraph("Title", heading_1()))
story.append(Spacer(1, 12))
story.append(Paragraph("Body text aligned justified.", arial_11_justified()))
doc.build(story)
```

Note: Fonts are loaded by relative paths (e.g., `fonts/arial.ttf`). Call `register_pdf_fonts()` before using styles.

## Install

Install the released version `v0.22` directly from GitHub:

```bash
pip install "git+https://github.com/spitoglou/stavros-lib.git@v0.22" -U
```


pip install git+https://github.com/spitoglou/stavros-lib.git -U