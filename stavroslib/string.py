"""String Manipulation Utilities"""

import re
import unicodedata


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug.

    Converts to lowercase, removes accents, replaces spaces/special characters
    with hyphens, and collapses multiple hyphens.

    Arguments:
        text: The text to slugify.

    Returns:
        A URL-safe slug (e.g., "hello-world").
    """
    # Remove accents
    text = remove_accents(text)
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special characters with hyphens
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    # Remove leading/trailing hyphens
    text = text.strip("-")
    return text


def truncate(text: str, max_len: int, suffix: str = "...") -> str:
    """Safely truncate text to a maximum length.

    Arguments:
        text: The text to truncate.
        max_len: The maximum length of the result (including suffix).
        suffix: The suffix to append if truncated (default: "...").

    Returns:
        The original text if it fits, or truncated text with suffix.
    """
    if len(text) <= max_len:
        return text
    if max_len <= len(suffix):
        return text[:max_len]
    return text[: max_len - len(suffix)] + suffix


def capitalize_words(text: str) -> str:
    """Capitalize the first letter of each word.

    Arguments:
        text: The text to capitalize.

    Returns:
        Text with each word capitalized.
    """
    if not text:
        return text
    return " ".join(word.capitalize() for word in text.split(" "))


def remove_accents(text: str) -> str:
    """Remove diacritical marks (accents) from Unicode characters.

    Arguments:
        text: The text to process.

    Returns:
        Text with accents removed.
    """
    nfkd_form = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd_form if unicodedata.category(c) != "Mn")
