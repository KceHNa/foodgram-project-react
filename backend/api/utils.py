from os import path

from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_NAME = 'shoppingcart'
FONT_SIZE_TITLE = 32
FONT_SIZE = 16
FONT_PATH = path.join(settings.BASE_DIR, f'data/{FONT_NAME}.ttf')
X_CENTER = 300
Y_CENTER = 800
X1_LINE = 100
Y1_LINE = 780
X2_LINE = 480
Y2_LINE = 780
HEIGHT = 750
INDENT = 75
SHOPPING_CART_TEMPLATE = '• {} ({}) - {}'


def create_pdf(shopping_cart):
    """
    Создает PDF-файл через reportlab
    """
    pdfmetrics.registerFont(
        TTFont(FONT_NAME, FONT_PATH, 'UTF-8')
    )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment;''filename="shopping_cart.pdf"'
    )
    pdf_doc = canvas.Canvas(response)
    pdf_doc.setTitle(settings.DOCUMENT_TITLE)
    pdf_doc.setFont(FONT_NAME, size=FONT_SIZE_TITLE)
    pdf_doc.drawCentredString(X_CENTER, Y_CENTER, 'Список покупок')
    pdf_doc.line(X1_LINE, Y1_LINE, X2_LINE, Y2_LINE)
    pdf_doc.setFont(FONT_NAME, size=FONT_SIZE)
    height = 750
    for ingredient in shopping_cart:
        pdf_doc.drawString(
            INDENT, height, (SHOPPING_CART_TEMPLATE.format(*ingredient))
        )
        height -= 25
    pdf_doc.showPage()
    pdf_doc.save()
    return response
