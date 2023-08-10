import io
import os
from unittest import TestCase

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
from pdf_to_tiny_book import main
from reportlab.lib.pagesizes import *
from reportlab.pdfgen import canvas


class Test(TestCase):
    def createFile(self, n):
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

        with open("C:\\Users\\neria\\Desktop\\בדיקות\\" + str(n) + "pages.pdf", "wb") as output_pdf:
            existing_pdf.write(output_pdf)
        output_pdf.close()

    def tests(self):
        r = "C:\\Users\\neria\\Desktop\בדיקות\\"
        r2 = 'pages.pdf'
        # משתנה שני(4, 8, 12, 16, 20, 24, 28, 32)
        # משתנה שלישי(2, 4, 8, 16)
        # משתנה רביעי('', 's')
        inputs1 = [r + '20' + r2, 32, 8, '', 'v', 0]  # זוגי פחות מגודל חוברת
        inputs2 = [r + '25' + r2, 16, 8, 's', 'v', 0]  # אי זוגי פחות מגודל חוברת
        inputs3 = [r + '33' + r2, 8, 8, 's', 'v', 0]  # אי זוגי גדול מגודל חוברת
        inputs4 = [r + '40' + r2, 4, 8, 's', 'v', 0]  # זוגי גדול מגודל חוברת
        inputs5 = [r + '64' + r2, 32, 4, 's', 'v', 0]  # זוגי שתי חוברות בדיוק
        inputs6 = [r + '101' + r2, 32, 4, 's', 'v', 0]  # אי זוגי יותר משתי חוברות

        main(inputs1)
        '''main(inputs2)
        main(inputs3)
        main(inputs4)
        main(inputs5)
        main(inputs6)'''

    def test_printText(self, n='20'):
        output1 = '7 223 26\n11 1825 4\n17 1229 0\n21 81 28\n9 205 24\n13 1623 6\n15 1427 2\n19 10'
        # output2 = ' \n0 \n15\n \n16 \n31 \n4 \n11\n \n20 \n27 \n10 \n5\n \n26 \n21 \n14 \n1\n \n30 \n17 \n2 \n13\n \n18 \n29 \n6 \n9\n \n22 \n25 \n8 \n7\n \n24 \n23 \n12 \n3\n \n28 \n19'
        # output3 = ' \n0 \n7\n \n18 \n21 \n10 \n13\n \n32 \n39 \n12 \n11\n \n38 \n33 \n6 \n1\n \n20 \n19 \n2 \n5\n \n24 \n31 \n16 \n23\n \n34 \n37 \n22 \n17\n \n36 \n35 \n4 \n3\n \n30 \n25 \n8 \n15\n \n26 \n29 \n5 \n5 \n14 \n9\n \n28 \n27'
        # output4 = ' \n0 \n3\n \n20 \n23 \n12 \n15\n \n32 \n35 \n14 \n13\n \n34 \n33 \n2 \n1\n \n22 \n21 \n4 \n7\n \n24 \n27 \n16 \n19\n \n36 \n39 \n18 \n17\n \n38 \n37 \n6 \n5\n \n26 \n25 \n8 \n11\n \n28 \n31 \n5 \n5 \n10 \n9\n \n30 \n29'
        # output5 = ''
        # output6 = ''
        tmp = "C:\\Users\\neria\\Desktop\\בדיקות"
        text = ''
        for a in os.listdir(tmp):
            if a.endswith(n + 'pages ready to print.pdf'):
                existing_pdf = PdfFileReader(open(tmp + '\\' + a, "rb"))
                for i in range(len(existing_pdf.pages)):
                    page = existing_pdf.pages[i]
                    text += page.extract_text()
                #text = text.replace('\n', '\\n')
                print(text)
                self.failUnlessEqual(output1, text)


'''if __name__ == '__main__':
    # createFile(20)
    # tests()
    test_printText('20')
'''
