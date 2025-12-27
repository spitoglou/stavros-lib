"""File and Path Utilities"""

from pathlib import Path
from typing import Sequence
import glob as glob_module


def ensure_dir(path: str) -> Path:
    """Create a directory if it does not exist.

    Arguments:
        path: The directory path to create.

    Returns:
        A Path object pointing to the directory.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """Read a text file and return its contents.

    Arguments:
        file_path: The path to the file to read.
        encoding: The text encoding to use (default: "utf-8").

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnicodeDecodeError: If the file cannot be decoded with the specified encoding.
    """
    with open(file_path, "r", encoding=encoding) as f:
        return f.read()


def write_file(file_path: str, content: str, encoding: str = "utf-8") -> None:
    """Write content to a text file, creating parent directories if needed.

    Arguments:
        file_path: The path to the file to write.
        content: The content to write.
        encoding: The text encoding to use (default: "utf-8").
    """
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)


def find_files(pattern: str, root: str = ".") -> list[str]:
    """Find files matching a glob pattern.

    Arguments:
        pattern: The glob pattern to match (e.g., "*.txt", "**/*.py").
        root: The root directory to search in (default: current directory).

    Returns:
        A list of relative paths matching the pattern.
    """
    root_path = Path(root)
    if not root_path.exists():
        return []

    # Handle recursive patterns (**/)
    if "**" in pattern:
        matches = glob_module.glob(str(root_path / pattern), recursive=True)
    else:
        matches = glob_module.glob(str(root_path / pattern))

    return sorted([str(Path(m).relative_to(root_path)) for m in matches])
