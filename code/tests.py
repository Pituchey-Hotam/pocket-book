import io
import json
import os
from math import sqrt, log
from unittest import TestCase

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
from pdf_to_tiny_book import *
from reportlab.lib.pagesizes import *
from reportlab.pdfgen import canvas


class Test(TestCase):
    dirT = f"C:\\Users\\{os.getenv('USERNAME')}\\בדיקות\\"

    def testCreateFiles(self):
        if not os.path.exists(self.dirT):
            os.mkdir(self.dirT)
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

            with open(self.dirT + str(n) + "pages.pdf", "wb") as output_pdf:
                existing_pdf.write(output_pdf)
            output_pdf.close()

    def tests(self):
        r2 = 'pages.pdf'
        # משתנה שני(4, 8, 12, 16, 20, 24, 28, 32)
        # משתנה שלישי(2, 4, 8, 16)
        # משתנה רביעי('', 's')
        inputs1 = [self.dirT + '20' + r2, 32, 8, '', 'v', 0]  # זוגי פחות מגודל חוברת
        inputs2 = [self.dirT + '25' + r2, 16, 8, 's', 'v', 0]  # אי זוגי פחות מגודל חוברת
        inputs3 = [self.dirT + '33' + r2, 8, 8, 's', 'v', 0]  # אי זוגי גדול מגודל חוברת
        inputs4 = [self.dirT + '40' + r2, 4, 8, 's', 'v', 0]  # זוגי גדול מגודל חוברת
        inputs5 = [self.dirT + '64' + r2, 32, 4, 's', 'v', 0]  # זוגי שתי חוברות בדיוק
        inputs6 = [self.dirT + '101' + r2, 32, 4, 's', 'v', 0]  # אי זוגי יותר משתי חוברות
        inputs7 = [self.dirT + '102' + r2, 32, 8, 's', 'v', 1]  # באנגלית
        # inputs8 = ['C:\\Users\\neria\\Desktop\\ללמוד לחזות התנהגות עתידית באמצעות רשתות חברתיות 1.pdf', 32, 8, 's', 'v', 0]  # באנגלית

        making_the_pdf(inputs1)
        making_the_pdf(inputs2)
        making_the_pdf(inputs3)
        making_the_pdf(inputs4)
        making_the_pdf(inputs5)
        making_the_pdf(inputs6)
        making_the_pdf(inputs7)
        # making_the_pdf(inputs8)

    def test_check(self):
        file = open('test.json', 'r')
        outputs = json.load(file)
        for a in os.listdir(self.dirT):
            text = ''
            if a.endswith('pages ready to print.pdf'):
                existing_pdf = PdfFileReader(open(self.dirT + '\\' + a, "rb"))
                for i in range(len(existing_pdf.pages)):
                    page = existing_pdf.pages[i]
                    text += page.extract_text()
                self.failUnlessEqual(outputs[a[:len('pages ready to print.pdf') * -1]], text,
                                     'output ' + a[:len('pages ready to print.pdf') * -1] + ' fail')


"""
    def testPrintOutputs(self):
        file = open('test.json', 'w')
        set1 = {}
        for a in os.listdir(self.dirT):
            text = ''
            if a.endswith('pages ready to print.pdf'):
                existing_pdf = PdfFileReader(open(self.dirT + '\\' + a, "rb"))
                for i in range(len(existing_pdf.pages)):
                    page = existing_pdf.pages[i]
                    text += page.extract_text()
                #text = text.replace('\n', '\\n')
                print(text + '\n' + a[:len('pages ready to print.pdf') * -1] + '\n')
                set1.update({a[:len('pages ready to print.pdf') * -1]: text})
        file.write(json.dumps(set1))"""
