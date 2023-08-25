import io
import os
import json
import pytest
from tempfile import mkdtemp

from PyPDF2 import PdfFileReader, PdfFileWriter
from src.pdf_to_tiny_book import making_the_pdf, PageSize
from reportlab.lib.pagesizes import *
from reportlab.pdfgen import canvas

test_dir = mkdtemp()
print(f"test_dir={test_dir}")

def create_test_pdf(pages_num):
    existing_pdf = PdfFileWriter()
    for i in range(pages_num):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFontSize(80)
        can.drawString(270, 200, str(i))
        can.save()
        packet.seek(0)
        # create a new PDF with Reportlab
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf.addBlankPage(A4[0], A4[1])
        # add the "watermark" (which is the new pdf) on the existing page
        existing_pdf.pages[i].merge_page(new_pdf.pages[0])
        # finally, write "output" to a real file

    test_file_path = os.path.join(test_dir, f"{pages_num}pages.pdf")
    with open(test_file_path, "wb") as f:
        existing_pdf.write(f)

    return test_file_path

@pytest.mark.parametrize("pages_num, notebook_len, page_size, bind_method, combine_method, language", [   
    (20, 32, PageSize.A7.value, '', 'v',0), # זוגי פחות מגודל חוברת
    (25, 16, PageSize.A7.value, 's', 'v', 0),  # אי זוגי פחות מגודל חוברת
    (33, 8, PageSize.A7.value, 's', 'v', 0),  # אי זוגי גדול מגודל חוברת
    (40, 4, PageSize.A7.value, 's', 'v', 0),  # זוגי גדול מגודל חוברת
    (64, 32, PageSize.A6.value, 's', 'v', 0),  # זוגי שתי חוברות בדיוק
    (101, 32, PageSize.A6.value, 's', 'v', 0),  # אי זוגי יותר משתי חוברות
    (102, 32, PageSize.A7.value, 's', 'v', 1),  # באנגלית
    # ['C:\\Users\\neria\\Desktop\\ללמוד לחזות התנהגות עתידית באמצעות רשתות חברתיות 1.pdf', 32, 8, 's', 'v', 0],  # באנגלית
])
def test_pocketing_book(pages_num, notebook_len, page_size, bind_method, combine_method, language):
    test_pdf_path = create_test_pdf(pages_num)

    making_the_pdf([test_pdf_path, notebook_len, page_size, bind_method, combine_method, language])

    with open(os.path.join("tests", "test_outputs.json"), 'r') as f:
        expected_outputs = json.load(f)

    pocketed_pdf_path = test_pdf_path[:-4] + " ready to print.pdf"
    pocketed_pdf = PdfFileReader(open(pocketed_pdf_path, "rb"))
    pdf_text=""
    for i in range(len(pocketed_pdf.pages)):
        page = pocketed_pdf.pages[i]
        pdf_text += page.extract_text()

    assert expected_outputs[str(pages_num)] == pdf_text
