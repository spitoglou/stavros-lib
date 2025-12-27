"""Tests for file utilities"""

import os
import tempfile
from pathlib import Path

from stavroslib.file import ensure_dir, find_files, read_file, write_file


class TestEnsureDir:
    def test_create_new_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "new_dir")
            result = ensure_dir(new_dir)
            assert Path(new_dir).exists()
            assert isinstance(result, Path)
            assert result == Path(new_dir)

    def test_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = ensure_dir(tmpdir)
            assert Path(tmpdir).exists()
            assert result == Path(tmpdir)

    def test_nested_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            nested = os.path.join(tmpdir, "a", "b", "c")
            result = ensure_dir(nested)
            assert Path(nested).exists()
            assert result == Path(nested)


class TestReadFile:
    def test_read_simple_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write("Hello World")
            temp_path = f.name

        try:
            content = read_file(temp_path)
            assert content == "Hello World"
        finally:
            os.unlink(temp_path)

    def test_read_multiline_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write("Line 1\nLine 2\nLine 3")
            temp_path = f.name

        try:
            content = read_file(temp_path)
            assert content == "Line 1\nLine 2\nLine 3"
        finally:
            os.unlink(temp_path)

    def test_read_file_not_found(self):
        try:
            read_file("/nonexistent/file.txt")
            assert False, "Expected FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_read_file_custom_encoding(self):
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, encoding="latin-1"
        ) as f:
            f.write("Hello World")
            temp_path = f.name

        try:
            content = read_file(temp_path, encoding="latin-1")
            assert content == "Hello World"
        finally:
            os.unlink(temp_path)

    def test_read_empty_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, encoding="utf-8"
        ) as f:
            temp_path = f.name

        try:
            content = read_file(temp_path)
            assert content == ""
        finally:
            os.unlink(temp_path)


class TestWriteFile:
    def test_write_new_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "output.txt")
            write_file(file_path, "Hello World")
            assert Path(file_path).exists()
            assert read_file(file_path) == "Hello World"

    def test_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "output.txt")
            write_file(file_path, "Original")
            write_file(file_path, "Updated")
            assert read_file(file_path) == "Updated"

    def test_create_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "a", "b", "c", "file.txt")
            write_file(file_path, "Content")
            assert Path(file_path).exists()
            assert read_file(file_path) == "Content"

    def test_write_multiline_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "output.txt")
            content = "Line 1\nLine 2\nLine 3"
            write_file(file_path, content)
            assert read_file(file_path) == content

    def test_write_custom_encoding(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "output.txt")
            write_file(file_path, "Hello", encoding="latin-1")
            assert read_file(file_path, encoding="latin-1") == "Hello"


class TestFindFiles:
    def test_find_simple_pattern(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            open(os.path.join(tmpdir, "file1.txt"), "w").close()
            open(os.path.join(tmpdir, "file2.txt"), "w").close()
            open(os.path.join(tmpdir, "file3.py"), "w").close()

            matches = find_files("*.txt", root=tmpdir)
            assert len(matches) == 2
            assert "file1.txt" in matches
            assert "file2.txt" in matches

    def test_find_recursive_pattern(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested structure
            subdir = os.path.join(tmpdir, "sub", "nested")
            os.makedirs(subdir)
            open(os.path.join(tmpdir, "file1.py"), "w").close()
            open(os.path.join(subdir, "file2.py"), "w").close()

            matches = find_files("**/*.py", root=tmpdir)
            assert len(matches) >= 2

    def test_find_no_matches(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            matches = find_files("*.xyz", root=tmpdir)
            assert matches == []

    def test_find_nonexistent_root(self):
        matches = find_files("*.txt", root="/nonexistent/path")
        assert matches == []

    def test_find_current_directory(self):
        # This test just verifies the default root works
        matches = find_files("*.py", root=".")
        # Should find some .py files in current directory (but may be empty in test)
        assert isinstance(matches, list)
