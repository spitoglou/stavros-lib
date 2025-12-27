# stavros-lib

A lightweight Python utility library providing modular, type-safe functions for common programming tasks. Built with Python 3.13, UV package management, and spec-driven development.

**Stats**: 11 modules • 95% test coverage • 100% type-safe • 9 capability specs

## Architecture

The library is organized into focused, domain-specific modules:
- **datetime.py** - Parse, format, and calculate relative times
- **dict.py** - Merge and manipulate dictionaries
- **file.py** - File operations (read/write, directory creation, glob patterns)
- **ftp.py** - FTP upload, monitoring, and directory operations
- **misc.py** - Miscellaneous utilities (country data, system notifications)
- **parse.py** - Configuration file parsing (YAML, TOML, .env)
- **pdf.py** - PDF generation with ReportLab fonts
- **probability.py** - Odds conversion and binomial probability calculations
- **string.py** - String manipulation (slugs, truncation, accent removal)
- **xml.py** - XML parsing and namespace removal

Each module is minimal, well-tested, and fully documented. External dependencies are minimal: stdlib plus requests, PyYAML, plyer, reportlab, and lxml.

## Setup

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

### Parse date/time strings

```python
from stavroslib.datetime import parse_datetime

dt = parse_datetime("2024-01-15T10:30:00Z")  # ISO 8601
dt = parse_datetime("15/01/2024")            # Common format
dt = parse_datetime("Jan 15, 2024")          # Human-readable
```

### Format datetime objects

```python
from datetime import datetime
from stavroslib.datetime import format_datetime

dt = datetime(2024, 1, 15, 10, 30, 0)
format_datetime(dt, preset="iso")    # "2024-01-15T10:30:00"
format_datetime(dt, preset="human")  # "January 15, 2024"
format_datetime(dt, preset="short")  # "01/15/24"
```

### Relative time descriptions

```python
from datetime import datetime, timedelta
from stavroslib.datetime import relative_time

past = datetime.now() - timedelta(hours=2)
future = datetime.now() + timedelta(days=3)

relative_time(past)    # "2 hours ago"
relative_time(future)  # "in 3 days"
```

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

### Read .env files

```python
from stavroslib.parse import read_env

env_vars = read_env(".env")
db_host = env_vars.get("DB_HOST", "localhost")
db_port = env_vars.get("DB_PORT", "5432")
```

Notes:
- Supports `KEY=VALUE`, comments (`#`), quotes, and `export` prefix
- Returns empty dict for empty file
- Raises `FileNotFoundError` if file doesn't exist

### Merge dictionaries

```python
from stavroslib.dict import merge_dicts

d1 = {"name": "Stavros"}
d2 = {"last": "Pitoglou"}
merged = merge_dicts(d1, d2)
# {"name": "Stavros", "last": "Pitoglou"}
```

### File utilities

```python
from stavroslib.file import ensure_dir, read_file, write_file, find_files

# Create directory if missing
ensure_dir("config/app")

# Read and write files with encoding support
content = read_file("config.txt", encoding="utf-8")
write_file("output.txt", "Hello World", encoding="utf-8")

# Find files by pattern
py_files = find_files("**/*.py", root="src")
config_files = find_files("*.toml")  # Current directory
```

### String utilities

```python
from stavroslib.string import slugify, truncate, capitalize_words, remove_accents

slugify("Hello World")                    # "hello-world"
slugify("Café au Lait")                  # "cafe-au-lait"

truncate("Hello World", max_len=8)        # "Hello..."
truncate("Hello World", max_len=8, suffix="…")  # "Hello W…"

capitalize_words("hello world")           # "Hello World"

remove_accents("Café Naïve")              # "Cafe Naive"
remove_accents("Niño Español")            # "Nino Espanol"
```

### XML utilities

```python
from stavroslib.xml import xml_to_dict, remove_namespace

# Parse XML to nested dict
xml = "<root><item id='1'>value</item></root>"
data = xml_to_dict(xml)
# {"root": {"item": {"@id": "1", "#text": "value"}}}

# Remove namespaces from XML
namespaced_xml = '<root xmlns="http://example.com"><item>value</item></root>'
clean_xml = remove_namespace(namespaced_xml)
# "<root><item>value</item></root>"
```

Notes:
- Attributes prefixed with `@`, text content uses `#text`
- Repeated elements become lists
- Namespace removal uses XSLT transformation

### Probability and odds conversion

```python
from stavroslib.probability import (
    convert_dec_to_prob,
    convert_prob_to_dec,
    convert_frac_to_prob,
    exact_binomial_probability,
    cumulative_binomial_probabilities
)

# Convert between odds formats
convert_dec_to_prob(2.5)      # 0.4 (decimal odds to probability)
convert_prob_to_dec(0.25)     # 4.0 (probability to decimal odds)
convert_frac_to_prob(3, 1)    # 0.25 (fractional 3/1 to probability)

# Binomial probabilities
prob = exact_binomial_probability(10, 5, 0.5)  # P(X = 5) for 10 trials
lt, lte, gt, gte = cumulative_binomial_probabilities(10, 5, 0.5)
# Returns P(X < 5), P(X <= 5), P(X > 5), P(X >= 5)
```

### FTP operations

```python
from stavroslib.ftp import upload_all, monitor_and_ftp, FtpHelper

# Upload directory to FTP server
success = upload_all(
    server="ftp.example.com",
    username="user",
    password="pass",
    local_dir="./output",
    remote_dir="/public_html",
    walk=True,  # Recursively upload subdirectories
    ignore_extensions=[".pyc", ".tmp"],
    on_upload=lambda path: print(f"Uploaded {path}"),
    on_error=lambda msg, exc: print(f"Error: {msg}")
)

# Monitor directory and auto-upload changes
try:
    monitor_and_ftp(
        server="ftp.example.com",
        username="user",
        password="pass",
        local_dir="./watch",
        remote_dir="/remote",
        sleep_seconds=2,
        on_change=lambda files: print(f"Changed: {files}")
    )
except KeyboardInterrupt:
    print("Monitoring stopped")
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