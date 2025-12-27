"""
Dictionary Operations
"""

from typing import Any


def merge_dicts(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """Merge 2 dictionaries

    Arguments:
        dict1 {dict} -- 1st Dictionary
        dict2 {dict} -- 2nd Dictionary

    Returns:
        dict -- Concatenated Dictionary
    """

    return {**dict1, **dict2}
