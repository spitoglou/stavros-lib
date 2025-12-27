from io import TextIOWrapper
from typing import Any
import re

import yaml
import tomllib


def read_yaml(file: str) -> dict[str, Any] | None:
    stream: TextIOWrapper = open(file, "r", encoding="utf8")
    result: dict[str, Any] | None = yaml.load(stream, Loader=yaml.FullLoader)
    return result


def read_toml(file: str) -> dict[str, Any] | None:
    """Read TOML file into a dict using stdlib tomllib.

    Returns None for empty files; raises tomllib.TOMLDecodeError on invalid TOML.
    """
    with open(file, "rb") as fp:
        data = fp.read()
        if data.strip() == b"":
            return None
        # TOML is UTF-8 per spec
        return tomllib.loads(data.decode("utf-8"))


def read_env(file_path: str) -> dict[str, str]:
    """Read .env file into a dictionary.

    Supports KEY=VALUE syntax, comments (#), quoted values (single/double),
    export prefix, and whitespace handling.

    Arguments:
        file_path: Path to the .env file.

    Returns:
        Dictionary of environment variables.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    env_vars: dict[str, str] = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Strip whitespace
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Remove export prefix if present
            if line.startswith("export "):
                line = line[7:].strip()

            # Split on first = sign
            if "=" not in line:
                continue

            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()

            # Remove inline comments (but not if inside quotes)
            if "#" in value:
                # Simple approach: only remove if not quoted
                if not (value.startswith('"') or value.startswith("'")):
                    value = value.split("#")[0].strip()

            # Remove quotes if present
            if len(value) >= 2:
                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    value = value[1:-1]

            env_vars[key] = value

    return env_vars
