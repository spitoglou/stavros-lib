from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.platypus.flowables import Image, Spacer


def register_pdf_fonts() -> None:
    pdfmetrics.registerFont(TTFont('Arial', 'fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialB', 'fonts/arial_bold.ttf'))
    pdfmetrics.registerFont(TTFont('ArialN', 'fonts/arial-narrow.ttf'))
    pdfmetrics.registerFont(TTFont('Courier', 'fonts/courier.ttf'))
    pdfmetrics.registerFont(TTFont('CourierB', 'fonts/courier_bold.ttf'))
    pdfmetrics.registerFont(TTFont('CourierNew', 'fonts/courier_new.ttf'))
    pdfmetrics.registerFont(
        TTFont('CourierNewB', 'fonts/courier_new_bold.ttf'))


def arial_11_justified():
    custom_body_style = getSampleStyleSheet()['BodyText']
    custom_body_style.fontName = 'Arial'
    custom_body_style.fontSize = 11
    custom_body_style.alignment = 4
    return custom_body_style


def arial_11_right():
    custom_body_style = getSampleStyleSheet()['BodyText']
    custom_body_style.fontName = 'Arial'
    custom_body_style.fontSize = 11
    custom_body_style.alignment = 2
    return custom_body_style


def heading_1():
    custom_body_style = getSampleStyleSheet()['Heading1']
    custom_body_style.fontName = 'Arial'
    return custom_body_style
