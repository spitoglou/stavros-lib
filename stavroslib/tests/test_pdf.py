from reportlab.lib.styles import ParagraphStyle

from stavroslib.pdf import (
    arial_11_justified,
    arial_11_right,
    heading_1,
)


def test_arial_11_justified():
    style = arial_11_justified()
    assert isinstance(style, ParagraphStyle)
    assert style.fontName == "Arial"
    assert style.fontSize == 11
    assert style.alignment == 4  # justified


def test_arial_11_right():
    style = arial_11_right()
    assert isinstance(style, ParagraphStyle)
    assert style.fontName == "Arial"
    assert style.fontSize == 11
    assert style.alignment == 2  # right


def test_heading_1():
    style = heading_1()
    assert isinstance(style, ParagraphStyle)
    assert style.fontName == "Arial"
