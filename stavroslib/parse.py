from io import TextIOWrapper
from typing import Any

import yaml


def read_yaml(file: str) -> dict[str, Any] | None:
    stream: TextIOWrapper = open(file, "r", encoding="utf8")
    result: dict[str, Any] | None = yaml.load(stream, Loader=yaml.FullLoader)
    return result
