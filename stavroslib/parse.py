from io import TextIOWrapper
from typing import Any

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
