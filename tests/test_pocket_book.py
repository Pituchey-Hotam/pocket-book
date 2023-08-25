import io
import os
import json
import pytest
from tempfile import mkdtemp

from PyPDF2 import PdfFileReader, PdfFileWriter
from src.pdf_to_tiny_book import *
from reportlab.lib.pagesizes import *
from reportlab.pdfgen import canvas

test_dir = mkdtemp()
print(f"test_dir={test_dir}")

def test_create_preprocessed_files():
    for n in [20, 25, 33, 40, 64, 101, 102]:
        existing_pdf = PdfFileWriter()
        for i in range(n):
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

        with open(os.path.join(test_dir, f"{n}pages.pdf"), "wb") as output_pdf:
            existing_pdf.write(output_pdf)
        output_pdf.close()

files_suffix = 'pages.pdf'

@pytest.mark.parametrize("inputs", [   
    # משתנה שני(4, 8, 12, 16, 20, 24, 28, 32)
    # משתנה שלישי(2, 4, 8, 16)
    # משתנה רביעי('', 's')
    [os.path.join(test_dir, f"20{files_suffix}"), 32, 8, '', 'v', 0] , # זוגי פחות מגודל חוברת
    [os.path.join(test_dir, f"25{files_suffix}"), 16, 8, 's', 'v', 0],  # אי זוגי פחות מגודל חוברת
    [os.path.join(test_dir, f"33{files_suffix}"), 8, 8, 's', 'v', 0],  # אי זוגי גדול מגודל חוברת
    [os.path.join(test_dir, f"40{files_suffix}"), 4, 8, 's', 'v', 0],  # זוגי גדול מגודל חוברת
    [os.path.join(test_dir, f"64{files_suffix}"), 32, 4, 's', 'v', 0],  # זוגי שתי חוברות בדיוק
    [os.path.join(test_dir, f"101{files_suffix}"), 32, 4, 's', 'v', 0],  # אי זוגי יותר משתי חוברות
    [os.path.join(test_dir, f"102{files_suffix}"), 32, 8, 's', 'v', 1],  # באנגלית
    # ['C:\\Users\\neria\\Desktop\\ללמוד לחזות התנהגות עתידית באמצעות רשתות חברתיות 1.pdf', 32, 8, 's', 'v', 0],  # באנגלית
])
def test_pocketing_book(inputs):
    making_the_pdf(inputs)

def test_pocketing_correctness():
    with open(os.path.join("tests", "test.json"), 'r') as f:
        outputs = json.load(f)

    pdfs = os.listdir(test_dir)
    assert len(pdfs) == 14, f"Got wrong number of pdfs, not testing all of them. len(pdf)={len(pdfs)}"

    suffix_len = len('pages ready to print.pdf')

    for pdf in pdfs:
        text = ''
        if pdf.endswith('pages ready to print.pdf'):
            existing_pdf = PdfFileReader(open(os.path.join(test_dir, pdf), "rb"))

            for i in range(len(existing_pdf.pages)):
                page = existing_pdf.pages[i]
                text += page.extract_text()

            assert outputs[pdf[:-suffix_len]] == text, f"output {pdf[:-suffix_len]} fail"



def print_outputs():
    """prints the outputs to see by eyes"""
    set1 = {}
    for a in os.listdir(test_dir):
        text = ''
        if a.endswith('pages ready to print.pdf'):
            existing_pdf = PdfFileReader(open(test_dir + '\\' + a, "rb"))
            for i in range(len(existing_pdf.pages)):
                page = existing_pdf.pages[i]
                text += page.extract_text()
            #text = text.replace('\n', '\\n')
            print(text + '\n' + a[:len('pages ready to print.pdf') * -1] + '\n')
            set1.update({a[:len('pages ready to print.pdf') * -1]: text})

    with open('test.json', 'w') as f:
        f.write(json.dumps(set1))
