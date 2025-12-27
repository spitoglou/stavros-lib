import os
import tempfile

from stavroslib.parse import read_env, read_yaml


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


class TestReadEnv:
    def test_simple_key_value(self):
        content = "KEY=value\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY": "value"}
        finally:
            os.unlink(temp_path)

    def test_comments(self):
        content = "# This is a comment\nKEY=value\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY": "value"}
        finally:
            os.unlink(temp_path)

    def test_inline_comments(self):
        content = "KEY=value # inline comment\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY": "value"}
        finally:
            os.unlink(temp_path)

    def test_double_quoted_values(self):
        content = 'KEY="value with spaces"\n'
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY": "value with spaces"}
        finally:
            os.unlink(temp_path)

    def test_single_quoted_values(self):
        content = "KEY='value'\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY": "value"}
        finally:
            os.unlink(temp_path)

    def test_empty_value(self):
        content = "KEY=\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY": ""}
        finally:
            os.unlink(temp_path)

    def test_empty_lines(self):
        content = "KEY1=value1\n\nKEY2=value2\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY1": "value1", "KEY2": "value2"}
        finally:
            os.unlink(temp_path)

    def test_whitespace_handling(self):
        content = "  KEY = value  \n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY": "value"}
        finally:
            os.unlink(temp_path)

    def test_export_syntax(self):
        content = "export KEY=value\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {"KEY": "value"}
        finally:
            os.unlink(temp_path)

    def test_file_not_found(self):
        try:
            read_env("/nonexistent/file.env")
            assert False, "Expected FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_empty_file(self):
        content = ""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_multiple_entries(self):
        content = """
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=admin
DB_PASS="secret password"
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False, encoding="utf8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = read_env(temp_path)
            assert result["DB_HOST"] == "localhost"
            assert result["DB_PORT"] == "5432"
            assert result["DB_NAME"] == "mydb"
            assert result["DB_USER"] == "admin"
            assert result["DB_PASS"] == "secret password"
        finally:
            os.unlink(temp_path)
