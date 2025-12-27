"""Tests for FTP utilities."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import ftplib
import pytest

from stavroslib.ftp import (
    FtpHelper,
    _get_local_files,
    monitor_and_ftp,
    upload_all,
)


class TestFtpHelper:
    """Test FtpHelper class."""

    def test_path_exists_true(self):
        """Test path_exists returns True for existing path."""
        mock_ftp = MagicMock()
        helper = FtpHelper(mock_ftp)

        result = helper.path_exists("/remote/path")

        assert result is True
        mock_ftp.cwd.assert_called_once_with("/remote/path")

    def test_path_exists_false(self):
        """Test path_exists returns False for non-existing path."""
        mock_ftp = MagicMock()
        mock_ftp.cwd.side_effect = ftplib.error_perm("550 No such directory")
        helper = FtpHelper(mock_ftp)

        result = helper.path_exists("/nonexistent")

        assert result is False

    def test_path_exists_caching(self):
        """Test that path_exists uses cache."""
        mock_ftp = MagicMock()
        helper = FtpHelper(mock_ftp)

        # First call
        helper.path_exists("/remote/path")
        assert mock_ftp.cwd.call_count == 1

        # Second call should use cache
        helper.path_exists("/remote/path")
        assert mock_ftp.cwd.call_count == 1  # Still 1, not 2

    def test_makedirs_creates_single_dir(self):
        """Test makedirs creates a single directory."""
        mock_ftp = MagicMock()
        mock_ftp.cwd.side_effect = ftplib.error_perm("550 No such directory")
        helper = FtpHelper(mock_ftp)

        helper.makedirs("/remote/newdir")

        # Should create /remote and /remote/newdir
        assert mock_ftp.mkd.call_count == 2

    def test_makedirs_creates_nested_dirs(self):
        """Test makedirs creates nested directories."""
        mock_ftp = MagicMock()
        mock_ftp.cwd.side_effect = ftplib.error_perm("550 No such directory")
        helper = FtpHelper(mock_ftp)

        helper.makedirs("/remote/path/to/dir")

        # Should create /remote, /remote/path, /remote/path/to, /remote/path/to/dir
        assert mock_ftp.mkd.call_count == 4

    def test_makedirs_skips_existing(self):
        """Test makedirs skips existing directories."""
        mock_ftp = MagicMock()
        helper = FtpHelper(mock_ftp)

        # First path exists
        calls = [None, ftplib.error_perm("550 No such directory")]
        mock_ftp.cwd.side_effect = calls

        helper.makedirs("/existing/newdir")

        # Should only try to create /existing/newdir (not /existing)
        assert mock_ftp.mkd.call_count == 1


class TestGetLocalFiles:
    """Test _get_local_files function."""

    def test_get_local_files_single_dir(self, tmp_path):
        """Test getting files from single directory."""
        # Create test files
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.py").write_text("content2")

        files = _get_local_files(str(tmp_path), walk=False)

        assert len(files) == 2
        paths = [f["path"] for f in files]
        assert any("file1.txt" in p for p in paths)
        assert any("file2.py" in p for p in paths)

    def test_get_local_files_with_walk(self, tmp_path):
        """Test getting files recursively."""
        # Create nested structure
        (tmp_path / "file1.txt").write_text("content1")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("content2")

        files = _get_local_files(str(tmp_path), walk=True)

        assert len(files) == 2

    def test_get_local_files_ignores_extensions(self, tmp_path):
        """Test ignoring specific file extensions."""
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.pyc").write_text("content2")
        (tmp_path / "file3.tmp").write_text("content3")

        files = _get_local_files(
            str(tmp_path), walk=False, ignore_extensions=[".pyc", ".tmp"]
        )

        assert len(files) == 1
        assert "file1.txt" in files[0]["path"]

    def test_get_local_files_ignores_dirs(self, tmp_path):
        """Test ignoring specific directories."""
        (tmp_path / "file1.txt").write_text("content1")
        ignored_dir = tmp_path / "__pycache__"
        ignored_dir.mkdir()
        (ignored_dir / "file2.pyc").write_text("content2")

        files = _get_local_files(str(tmp_path), walk=True, ignore_dirs=["__pycache__"])

        assert len(files) == 1
        assert "__pycache__" not in files[0]["path"]

    def test_get_local_files_has_mtime(self, tmp_path):
        """Test that files have modification time."""
        (tmp_path / "file1.txt").write_text("content1")

        files = _get_local_files(str(tmp_path), walk=False)

        assert len(files) == 1
        assert "mtime" in files[0]
        assert isinstance(files[0]["mtime"], float)


class TestUploadAll:
    """Test upload_all function."""

    @patch("stavroslib.ftp.ftplib.FTP")
    def test_upload_all_success(self, mock_ftp_class, tmp_path):
        """Test successful upload."""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # Setup mock
        mock_ftp = MagicMock()
        mock_ftp_class.return_value = mock_ftp

        result = upload_all(
            "ftp.example.com",
            "user",
            "pass",
            str(tmp_path),
            "/remote",
            walk=False,
        )

        assert result is True
        mock_ftp.connect.assert_called_once_with("ftp.example.com")
        mock_ftp.login.assert_called_once_with("user", "pass")
        mock_ftp.quit.assert_called_once()

    @patch("stavroslib.ftp.ftplib.FTP")
    def test_upload_all_connection_failure(self, mock_ftp_class, tmp_path):
        """Test upload with connection failure."""
        (tmp_path / "test.txt").write_text("content")

        mock_ftp = MagicMock()
        mock_ftp.connect.side_effect = OSError("Connection failed")
        mock_ftp_class.return_value = mock_ftp

        error_callback = Mock()
        result = upload_all(
            "ftp.example.com",
            "user",
            "pass",
            str(tmp_path),
            "/remote",
            on_error=error_callback,
        )

        assert result is False
        error_callback.assert_called()

    @patch("stavroslib.ftp.ftplib.FTP")
    def test_upload_all_auth_failure(self, mock_ftp_class, tmp_path):
        """Test upload with authentication failure."""
        (tmp_path / "test.txt").write_text("content")

        mock_ftp = MagicMock()
        mock_ftp.login.side_effect = ftplib.error_perm("Login incorrect")
        mock_ftp_class.return_value = mock_ftp

        error_callback = Mock()
        result = upload_all(
            "ftp.example.com",
            "user",
            "wrongpass",
            str(tmp_path),
            "/remote",
            on_error=error_callback,
        )

        assert result is False
        error_callback.assert_called()

    @patch("stavroslib.ftp.ftplib.FTP")
    def test_upload_all_with_callbacks(self, mock_ftp_class, tmp_path):
        """Test upload with callbacks."""
        (tmp_path / "test.txt").write_text("content")

        mock_ftp = MagicMock()
        mock_ftp_class.return_value = mock_ftp

        upload_callback = Mock()
        result = upload_all(
            "ftp.example.com",
            "user",
            "pass",
            str(tmp_path),
            "/remote",
            on_upload=upload_callback,
        )

        assert result is True
        upload_callback.assert_called()

    @patch("stavroslib.ftp.ftplib.FTP")
    def test_upload_all_empty_directory(self, mock_ftp_class, tmp_path):
        """Test upload with empty directory."""
        error_callback = Mock()
        result = upload_all(
            "ftp.example.com",
            "user",
            "pass",
            str(tmp_path),
            "/remote",
            on_error=error_callback,
        )

        assert result is False
        error_callback.assert_called()

    @patch("stavroslib.ftp.ftplib.FTP")
    def test_upload_all_with_ignore_extensions(self, mock_ftp_class, tmp_path):
        """Test upload with ignored extensions."""
        (tmp_path / "file.txt").write_text("keep")
        (tmp_path / "file.pyc").write_text("ignore")

        mock_ftp = MagicMock()
        mock_ftp_class.return_value = mock_ftp

        result = upload_all(
            "ftp.example.com",
            "user",
            "pass",
            str(tmp_path),
            "/remote",
            ignore_extensions=[".pyc"],
        )

        assert result is True
        # Should only upload one file (file.txt)
        assert mock_ftp.storbinary.call_count == 1


class TestMonitorAndFtp:
    """Test monitor_and_ftp function."""

    @patch("stavroslib.ftp.time.sleep")
    @patch("stavroslib.ftp._upload_specific_files")
    @patch("stavroslib.ftp._get_local_files")
    def test_monitor_and_ftp_detects_changes(
        self, mock_get_files, mock_upload, mock_sleep, tmp_path
    ):
        """Test that monitor detects file changes."""
        # Simulate file list changing
        file1 = {"path": str(tmp_path / "test.txt"), "mtime": 100.0}
        file1_modified = {"path": str(tmp_path / "test.txt"), "mtime": 200.0}

        mock_get_files.side_effect = [
            [file1],  # Initial
            [file1],  # First check (no change)
            [file1_modified],  # Second check (changed)
            KeyboardInterrupt,  # Exit
        ]
        mock_upload.return_value = True

        on_change_callback = Mock()

        with pytest.raises(KeyboardInterrupt):
            monitor_and_ftp(
                "ftp.example.com",
                "user",
                "pass",
                str(tmp_path),
                "/remote",
                sleep_seconds=1,
                on_change=on_change_callback,
            )

        # Should detect one change
        on_change_callback.assert_called_once()

    @patch("stavroslib.ftp.time.sleep")
    @patch("stavroslib.ftp._upload_specific_files")
    @patch("stavroslib.ftp._get_local_files")
    def test_monitor_and_ftp_keyboard_interrupt(
        self, mock_get_files, mock_upload, mock_sleep, tmp_path
    ):
        """Test that monitor handles KeyboardInterrupt."""
        file1 = {"path": str(tmp_path / "test.txt"), "mtime": 100.0}
        mock_get_files.return_value = [file1]
        mock_sleep.side_effect = KeyboardInterrupt

        with pytest.raises(KeyboardInterrupt):
            monitor_and_ftp("ftp.example.com", "user", "pass", str(tmp_path), "/remote")
