"""FTP Upload and Monitoring Utilities"""

import ftplib
import os
import socket
import time
from typing import Callable, TypedDict


class FileInfo(TypedDict):
    """File information with path and modification time."""

    path: str
    mtime: float


class FtpHelper:
    """Helper class for FTP operations like path checking and directory creation."""

    def __init__(self, ftp_handle: ftplib.FTP):
        """Initialize FTP helper.

        Arguments:
            ftp_handle: Active FTP connection object.
        """
        self.ftp_handle = ftp_handle
        self._path_cache: list[str] = []

    def path_exists(self, path: str) -> bool:
        """Check if a path exists on the FTP server.

        Arguments:
            path: Remote path to check.

        Returns:
            True if path exists, False otherwise.
        """
        if path in self._path_cache:
            return True

        try:
            self.ftp_handle.cwd(path)
            self._path_cache.append(path)
            return True
        except ftplib.error_perm:
            return False

    def makedirs(self, path: str, sep: str = "/") -> None:
        """Create remote directories recursively (like mkdir -p).

        Arguments:
            path: Remote path to create.
            sep: Path separator (default: "/").
        """
        split_path = path.split(sep)
        new_dir = ""

        for server_dir in split_path:
            if server_dir:
                new_dir += sep + server_dir
                if not self.path_exists(new_dir):
                    try:
                        self.ftp_handle.mkd(new_dir)
                    except ftplib.error_perm:
                        # Directory might already exist or permission denied
                        pass


def _get_local_files(
    local_dir: str,
    walk: bool = False,
    ignore_dirs: list[str] | None = None,
    ignore_files: list[str] | None = None,
    ignore_extensions: list[str] | None = None,
) -> list[FileInfo]:
    """Get list of local files with modification times.

    Arguments:
        local_dir: Local directory to scan.
        walk: If True, recursively scan subdirectories.
        ignore_dirs: List of directory names to ignore.
        ignore_files: List of file names to ignore.
        ignore_extensions: List of file extensions to ignore (e.g., ['.pyc', '.tmp']).

    Returns:
        List of dicts with 'path' and 'mtime' keys.
    """
    if ignore_dirs is None:
        ignore_dirs = [".git", ".svn", "CVS", "__pycache__"]
    if ignore_files is None:
        ignore_files = [".DS_Store", "Thumbs.db"]
    if ignore_extensions is None:
        ignore_extensions = []

    result_list = []
    base_dir = os.path.abspath(local_dir)

    for current_dir, dirs, files in os.walk(base_dir):
        # Remove ignored directories from the walk
        for this_dir in ignore_dirs:
            if this_dir in dirs:
                dirs.remove(this_dir)

        sub_dir = current_dir.replace(base_dir, "")
        if not walk and sub_dir:
            break

        for this_file in files:
            if this_file not in ignore_files:
                file_ext = os.path.splitext(this_file)[-1].lower()
                if file_ext not in ignore_extensions:
                    filepath = os.path.join(current_dir, this_file)
                    file_monitor_dict: FileInfo = {
                        "path": filepath,
                        "mtime": os.path.getmtime(filepath),
                    }
                    result_list.append(file_monitor_dict)

    return result_list


def upload_all(
    server: str,
    username: str,
    password: str,
    local_dir: str,
    remote_dir: str,
    walk: bool = False,
    ignore_dirs: list[str] | None = None,
    ignore_files: list[str] | None = None,
    ignore_extensions: list[str] | None = None,
    on_upload: Callable[[str], None] | None = None,
    on_error: Callable[[str, Exception], None] | None = None,
) -> bool:
    """Upload all files from local directory to FTP server.

    Arguments:
        server: FTP server hostname.
        username: FTP username.
        password: FTP password.
        local_dir: Local directory to upload from.
        remote_dir: Remote directory to upload to.
        walk: If True, recursively upload subdirectories.
        ignore_dirs: List of directory names to ignore.
        ignore_files: List of file names to ignore.
        ignore_extensions: List of file extensions to ignore.
        on_upload: Optional callback called for each uploaded file with filepath.
        on_error: Optional callback called on errors with (message, exception).

    Returns:
        True if upload succeeded, False otherwise.
    """
    local_dir = os.path.abspath(local_dir)
    remote_dir = os.path.normpath(remote_dir)

    local_files = _get_local_files(
        local_dir, walk, ignore_dirs, ignore_files, ignore_extensions
    )

    if not local_files:
        if on_error:
            on_error(f"No files found in {local_dir}", FileNotFoundError())
        return False

    ftp = ftplib.FTP()

    try:
        # Connect to server
        try:
            ftp.connect(server)
        except (socket.gaierror, OSError) as e:
            if on_error:
                on_error(f"Could not connect to {server}", e)
            return False

        # Login
        try:
            ftp.login(username, password)
        except ftplib.error_perm as e:
            if on_error:
                on_error("Authentication failed", e)
            return False

        ftp_helper = FtpHelper(ftp)

        # Upload files
        for file_info in local_files:
            filepath = file_info["path"]
            path, filename = os.path.split(filepath)
            remote_sub_path = path.replace(local_dir, "")
            remote_path = path.replace(local_dir, remote_dir)
            remote_path = remote_path.replace("\\", "/")  # Unix-style paths

            # Create remote directory if needed
            if not ftp_helper.path_exists(remote_path):
                ftp_helper.makedirs(remote_path)

            # Change to remote directory
            try:
                ftp.cwd(remote_path)
            except ftplib.error_perm as e:
                if on_error:
                    on_error(f"Cannot change to directory {remote_path}", e)
                continue

            # Upload file
            if os.path.exists(filepath):
                try:
                    with open(filepath, "rb") as f:
                        ftp.storbinary(f"STOR {filename}", f)
                    if on_upload:
                        display_path = os.path.join(remote_sub_path, filename).replace(
                            "\\", "/"
                        )
                        on_upload(display_path)
                except Exception as e:
                    if on_error:
                        on_error(f"Failed to upload {filepath}", e)
            else:
                if on_error:
                    on_error(f"File no longer exists: {filepath}", FileNotFoundError())

        ftp.quit()
        return True

    except Exception as e:
        if on_error:
            on_error("Upload failed", e)
        try:
            ftp.quit()
        except:
            pass
        return False


def monitor_and_ftp(
    server: str,
    username: str,
    password: str,
    local_dir: str,
    remote_dir: str,
    walk: bool = False,
    sleep_seconds: int = 1,
    on_change: Callable[[list[str]], None] | None = None,
    on_error: Callable[[str, Exception], None] | None = None,
) -> None:
    """Monitor local directory and upload changed files to FTP server.

    Continuously monitors the local directory for file changes and uploads
    modified files. Runs until interrupted (Ctrl+C).

    Arguments:
        server: FTP server hostname.
        username: FTP username.
        password: FTP password.
        local_dir: Local directory to monitor.
        remote_dir: Remote directory to upload to.
        walk: If True, recursively monitor subdirectories.
        sleep_seconds: Seconds to wait between checks (default: 1).
        on_change: Optional callback called with list of changed file paths.
        on_error: Optional callback called on errors with (message, exception).

    Raises:
        KeyboardInterrupt: When user interrupts with Ctrl+C.
    """
    last_files_list = _get_local_files(local_dir, walk)

    while True:
        try:
            time.sleep(sleep_seconds)

            latest_files_list = _get_local_files(local_dir, walk)
            files_to_update = []

            # Check for new or modified files
            for idx, latest_file in enumerate(latest_files_list):
                if idx < len(last_files_list):
                    # Compare modification times
                    if latest_file["mtime"] > last_files_list[idx]["mtime"]:
                        files_to_update.append(latest_file)
                else:
                    # New file
                    files_to_update.append(latest_file)

            # Upload changed files
            if files_to_update:
                if on_change:
                    changed_paths = [f["path"] for f in files_to_update]
                    on_change(changed_paths)

                # Upload using the same logic as upload_all but with specific files
                success = _upload_specific_files(
                    server,
                    username,
                    password,
                    local_dir,
                    remote_dir,
                    files_to_update,
                    on_error,
                )

                if not success:
                    break

            last_files_list = latest_files_list.copy()

        except KeyboardInterrupt:
            raise


def _upload_specific_files(
    server: str,
    username: str,
    password: str,
    local_dir: str,
    remote_dir: str,
    files_to_update: list[FileInfo],
    on_error: Callable[[str, Exception], None] | None = None,
) -> bool:
    """Internal helper to upload specific files."""
    ftp = ftplib.FTP()

    try:
        ftp.connect(server)
        ftp.login(username, password)
        ftp_helper = FtpHelper(ftp)

        for file_info in files_to_update:
            filepath = file_info["path"]
            path, filename = os.path.split(filepath)
            remote_path = path.replace(local_dir, remote_dir).replace("\\", "/")

            if not ftp_helper.path_exists(remote_path):
                ftp_helper.makedirs(remote_path)

            ftp.cwd(remote_path)

            if os.path.exists(filepath):
                try:
                    with open(filepath, "rb") as f:
                        ftp.storbinary(f"STOR {filename}", f)
                except Exception as e:
                    if on_error:
                        on_error(f"Failed to upload {filepath}", e)

        ftp.quit()
        return True

    except Exception as e:
        if on_error:
            on_error("Upload failed", e)
        try:
            ftp.quit()
        except:
            pass
        return False
