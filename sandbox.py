from stavroslib.pdf import register_pdf_fonts
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import Image, Spacer
from reportlab.platypus.tables import Table

if __name__ == '__main__':
    register_pdf_fonts()
