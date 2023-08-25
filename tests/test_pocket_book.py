import io
import os
import json
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

def test_pocketing_book():
    r2 = 'pages.pdf'
    # משתנה שני(4, 8, 12, 16, 20, 24, 28, 32)
    # משתנה שלישי(2, 4, 8, 16)
    # משתנה רביעי('', 's')
    inputs1 = [os.path.join(test_dir, f"20{r2}"), 32, 8, '', 'v', 0]  # זוגי פחות מגודל חוברת
    inputs2 = [os.path.join(test_dir, f"25{r2}"), 16, 8, 's', 'v', 0]  # אי זוגי פחות מגודל חוברת
    inputs3 = [os.path.join(test_dir, f"33{r2}"), 8, 8, 's', 'v', 0]  # אי זוגי גדול מגודל חוברת
    inputs4 = [os.path.join(test_dir, f"40{r2}"), 4, 8, 's', 'v', 0]  # זוגי גדול מגודל חוברת
    inputs5 = [os.path.join(test_dir, f"64{r2}"), 32, 4, 's', 'v', 0]  # זוגי שתי חוברות בדיוק
    inputs6 = [os.path.join(test_dir, f"101{r2}"), 32, 4, 's', 'v', 0]  # אי זוגי יותר משתי חוברות
    inputs7 = [os.path.join(test_dir, f"102{r2}"), 32, 8, 's', 'v', 1]  # באנגלית
    # inputs8 = ['C:\\Users\\neria\\Desktop\\ללמוד לחזות התנהגות עתידית באמצעות רשתות חברתיות 1.pdf', 32, 8, 's', 'v', 0]  # באנגלית

    making_the_pdf(inputs1)
    making_the_pdf(inputs2)
    making_the_pdf(inputs3)
    making_the_pdf(inputs4)
    making_the_pdf(inputs5)
    making_the_pdf(inputs6)
    making_the_pdf(inputs7)
    # making_the_pdf(inputs8)

def test_pocketing_correctness():
    file = open(os.path.join("tests", "test.json"), 'r')
    outputs = json.load(file)
    for a in os.listdir(test_dir):
        text = ''
        if a.endswith('pages ready to print.pdf'):
            existing_pdf = PdfFileReader(open(test_dir + '\\' + a, "rb"))
            for i in range(len(existing_pdf.pages)):
                page = existing_pdf.pages[i]
                text += page.extract_text()

            assert outputs[a[:len('pages ready to print.pdf') * -1]] == text, 'output ' + a[:len('pages ready to print.pdf') * -1] + ' fail'


"""
def test_print_outputs():
    'prints the outputs to see by eyes' 
    file = open('test.json', 'w')
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
    file.write(json.dumps(set1))"""
