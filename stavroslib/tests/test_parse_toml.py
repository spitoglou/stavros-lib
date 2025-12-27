import os
import tempfile
import tomllib

from stavroslib.parse import read_toml


def test_read_toml_simple():
    content = """
name = "Stavros"
age = 30
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        result = read_toml(temp_path)
        assert result == {"name": "Stavros", "age": 30}
    finally:
        os.unlink(temp_path)


def test_read_toml_nested():
    content = """
[database]
host = "localhost"
port = 5432

[database.credentials]
user = "admin"
password = "secret"
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        result = read_toml(temp_path)
        assert result is not None
        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 5432
        assert result["database"]["credentials"]["user"] == "admin"
    finally:
        os.unlink(temp_path)


def test_read_toml_list():
    content = """
fruits = ["apple", "banana", "orange"]
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        result = read_toml(temp_path)
        assert result is not None
        assert result["fruits"] == ["apple", "banana", "orange"]
    finally:
        os.unlink(temp_path)


def test_read_toml_empty():
    content = ""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        result = read_toml(temp_path)
        assert result is None
    finally:
        os.unlink(temp_path)


def test_read_toml_invalid():
    # Missing closing quote
    content = """
name = "Stavros
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", delete=False, encoding="utf8"
    ) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        try:
            _ = read_toml(temp_path)
            assert False, "Expected TOMLDecodeError"
        except tomllib.TOMLDecodeError:
            pass
    finally:
        os.unlink(temp_path)
