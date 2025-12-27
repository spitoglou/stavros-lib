"""Tests for string utilities"""

from stavroslib.string import (
    capitalize_words,
    remove_accents,
    slugify,
    truncate,
)


class TestSlugify:
    def test_simple_text(self):
        assert slugify("Hello World") == "hello-world"

    def test_with_special_characters(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_with_accents(self):
        assert slugify("Café au Lait") == "cafe-au-lait"

    def test_multiple_spaces(self):
        assert slugify("Hello    World") == "hello-world"

    def test_with_numbers(self):
        assert slugify("Test 123 Slug") == "test-123-slug"

    def test_mixed_case_and_special(self):
        assert slugify("My_Test@Slug!") == "my_testslug"

    def test_empty_string(self):
        assert slugify("") == ""

    def test_only_special_characters(self):
        assert slugify("!!!") == ""

    def test_leading_trailing_hyphens(self):
        assert slugify("--Hello--") == "hello"


class TestTruncate:
    def test_text_within_limit(self):
        assert truncate("Hello", max_len=10) == "Hello"

    def test_text_exceeds_limit(self):
        result = truncate("Hello World", max_len=8)
        assert result == "Hello..."
        assert len(result) == 8

    def test_custom_suffix(self):
        result = truncate("Hello World", max_len=9, suffix="…")
        assert result == "Hello Wo…"
        assert len(result) == 9

    def test_exact_fit(self):
        result = truncate("Hello", max_len=5)
        assert result == "Hello"

    def test_zero_max_len(self):
        result = truncate("Hello", max_len=0)
        assert result == "Hello"[:0]

    def test_max_len_less_than_suffix(self):
        result = truncate("Hello World", max_len=2, suffix="...")
        assert len(result) == 2

    def test_empty_string(self):
        assert truncate("", max_len=10) == ""

    def test_custom_long_suffix(self):
        result = truncate("Hello World", max_len=20, suffix=" [read more]")
        assert result == "Hello World"  # fits without truncation


class TestCapitalizeWords:
    def test_simple_text(self):
        assert capitalize_words("hello world") == "Hello World"

    def test_mixed_case(self):
        assert capitalize_words("heLLo WoRLd") == "Hello World"

    def test_with_hyphens(self):
        result = capitalize_words("hello-world test")
        # Hyphens don't split words; each space-separated token is capitalized
        assert result == "Hello-world Test"

    def test_single_word(self):
        assert capitalize_words("hello") == "Hello"

    def test_empty_string(self):
        assert capitalize_words("") == ""

    def test_multiple_spaces(self):
        result = capitalize_words("hello   world")
        # Should handle multiple spaces gracefully
        assert "Hello" in result and "World" in result

    def test_already_capitalized(self):
        assert capitalize_words("Hello World") == "Hello World"


class TestRemoveAccents:
    def test_french_accents(self):
        assert remove_accents("Café Naïve Résumé") == "Cafe Naive Resume"

    def test_spanish_accents(self):
        assert remove_accents("Niño Español") == "Nino Espanol"

    def test_no_accents(self):
        assert remove_accents("Hello World") == "Hello World"

    def test_mixed_accents(self):
        assert remove_accents("Ångström café") == "Angstrom cafe"

    def test_german_umlauts(self):
        # Note: German ß (sharp s) is not an accent mark, it's a separate letter
        assert remove_accents("Schön Grüß Äpfel") == "Schon Gruß Apfel"

    def test_empty_string(self):
        assert remove_accents("") == ""

    def test_numbers_and_special_chars(self):
        result = remove_accents("Café123!@#")
        assert result == "Cafe123!@#"

    def test_single_accented_char(self):
        assert remove_accents("é") == "e"

    def test_grave_accent(self):
        assert remove_accents("à") == "a"

    def test_circumflex(self):
        assert remove_accents("ô") == "o"
