import os
import tempfile

from stavroslib.parse import read_yaml


def test_read_yaml_simple():
    content = """
name: Stavros
age: 30
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        result = read_yaml(temp_path)
        assert result == {"name": "Stavros", "age": 30}
    finally:
        os.unlink(temp_path)


def test_read_yaml_nested():
    content = """
database:
  host: localhost
  port: 5432
  credentials:
    user: admin
    password: secret
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        result = read_yaml(temp_path)
        assert result is not None
        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 5432
        assert result["database"]["credentials"]["user"] == "admin"
    finally:
        os.unlink(temp_path)


def test_read_yaml_list():
    content = """
fruits:
  - apple
  - banana
  - orange
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        result = read_yaml(temp_path)
        assert result is not None
        assert result["fruits"] == ["apple", "banana", "orange"]
    finally:
        os.unlink(temp_path)


def test_read_yaml_empty():
    content = ""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        result = read_yaml(temp_path)
        assert result is None
    finally:
        os.unlink(temp_path)
