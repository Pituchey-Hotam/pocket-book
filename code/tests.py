import io
import os
from math import sqrt, log
from unittest import TestCase

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
from pdf_to_tiny_book import *
from reportlab.lib.pagesizes import *
from reportlab.pdfgen import canvas


class Test(TestCase):
    dirT = f"C:\\Users\\{os.getenv('USERNAME')}\\בדיקות\\"

    def testCreateFile(self):
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

        making_the_pdf(inputs1)
        making_the_pdf(inputs2)
        making_the_pdf(inputs3)
        making_the_pdf(inputs4)
        making_the_pdf(inputs5)
        making_the_pdf(inputs6)
        making_the_pdf(inputs7)

    def test_check(self):
        output1 = '7 223 26\n11 1825 4\n17 1229 0\n21 81 28\n9 205 24\n13 1623 6\n15 1427 2\n19 10'
        output2 = '0 15\n16 314 11\n20 2710 5\n26 2114 1\n30 172 13\n18 296 9\n22 258 7\n24 2312 3\n28 19'
        output3 = '0 7\n18 2110 13\n32 3912 11\n38 336 1\n20 192 5\n24 3116 23\n34 3722 17\n36 354 3\n30 258 15\n26 295514 9\n28 27'
        output4 = '0 3\n20 2312 15\n32 3514 13\n34 332 1\n22 214 7\n24 2716 19\n36 3918 17\n38 376 5\n26 258 11\n28 315510 9\n30 29'
        output5 = '0 31\n32 6330 1\n62 332 29\n34 6128 3\n60 354 27\n36 5926 5\n58 376 25\n38 5724 7\n56 398 23\n40 5522 9\n54 4110 21\n42 5320 11\n52 4312 19\n44 5118 13\n50 4514 17\n46 4916 15\n48 47'
        output6 = '0 31\n64 9530 1\n94 652 29\n66 9328 3\n92 674 27\n68 9126 5\n90 696 25\n70 8924 7\n88 718 23\n72 8722 9\n86 7310 21\n74 8520 11\n84 7512 19\n76 8318 13\n82 7714 17\n78 8116 15\n80 7932 63\n96 12762 33\n126 9734 61\n98 12560 35\n124 9936 59\n100 12358 37\n122 10138 57\n102 12156 39\n120 10340 55\n104 11954 41\n118 10542 53\n106 11752 43\n116 10744 51\n108 11550 45\n114 10946 49\n110 11348 47\n112 111'
        output7 = '127 96\n63 3295 64\n31 065 94\n1 3097 126\n33 62125 98\n61 3493 66\n29 267 92\n3 2899 124\n35 60123 100\n59 3691 68\n27 469 90\n5 26101 122\n37 58121 102\n57 3889 70\n25 671 88\n7 24103 120\n39 56119 104\n55 4087 72\n23 873 86\n9 22105 118\n41 54117 106\n53 4285 74\n21 1075 84\n11 20107 116\n43 52115 108\n51 4483 76\n19 1277 82\n13 18109 114\n45 50113 110\n49 4681 78\n17 1479 80\n15 16111 112\n47 48'
        outputs = {20: output1, 25: output2, 33: output3, 40: output4, 64: output5, 101: output6, 102: output7}
        for a in os.listdir(self.dirT):
            text = ''
            if a.endswith('pages ready to print.pdf'):
                existing_pdf = PdfFileReader(open(self.dirT + '\\' + a, "rb"))
                for i in range(len(existing_pdf.pages)):
                    page = existing_pdf.pages[i]
                    text += page.extract_text()
                # text = text.replace('\n', '\\n')
                # print(text)
                self.failUnlessEqual(outputs[int(a[:len('pages ready to print.pdf') * -1])], text,
                                     'output ' + a[:len('pages ready to print.pdf') * -1] + ' fail')

    def testPrintOutputs(self):
        for a in os.listdir(self.dirT):
            text = ''
            if a.endswith('pages ready to print.pdf'):
                existing_pdf = PdfFileReader(open(self.dirT + '\\' + a, "rb"))
                for i in range(len(existing_pdf.pages)):
                    page = existing_pdf.pages[i]
                    text += page.extract_text()
                text = text.replace('\n', '\\n')
                print(text + '\n' + a[:len('pages ready to print.pdf') * -1] + '\n')
