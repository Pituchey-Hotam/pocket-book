from pdfbooklet_new import *
# from ui_settings import *
# from pocket_book import *
import os
from io import BytesIO
from pocket_book import making_the_pdf
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file


class PdfFormQuestions:
    def __init__(self, page_types, merge_types, book_languages):
        self.page_types = page_types
        self.merge_types = merge_types
        self.book_languages = book_languages

# Version - important
currentVersion = "2.1.2"

ENGLISH_TEXT =  [
    "booklet project",
    "Choose a file: ",
    "Enter number of pages in each booklet (In multiples of 4. the standard is 32): ",
    "Enter pages per sheet (2/4/8/16): ",
    "Sewing or gluing? In the gluing there is an extra blank page on each side.",
    "only one notebook?",
    "DG & MM mini books maker " + currentVersion,
    "gluing",
    "Sewing",
    "page type",
    "create booklet",
    "Yes",
    "No",
    "Hebrew",
    "English",
    "Book language?",
    "Do it"
]

HEBREW_TEXT = [
    "פרויקט ספרי כיס",
    "בחר קובץ",
    "הכנס את מספר העמודים בכל מחברת (בכפולות של 4, הסטנדרט הוא 32)",
    "הכנס מספר עמודים לעמוד (2/4/8/16)",
    "מודבק או תפור? בגרסא המודבקת יש תוספת של עמוד ריק בכל מחברת",
    "האם כבודו מדפיס רק מחברת אחת?",
    "יוצר הספרונים של דביר ומלאכי" + currentVersion,
    "מודבק",
    "תפור",
    "סוג עמוד",
    "צור ספר כיס",
    "כן",
    "לא",
    "עברית",
    "אנגלית",
    "באיזו שפה הספר?",
    "יאללה לעבודה"
]


class PdfFormText:
    def __init__(self, language):
        if language == 'english':
            text = ENGLISH_TEXT
            self.language_format = ['en', 'ltr']
            self.booklet_parameters = 'booklet parameters'
        else:
            text = HEBREW_TEXT
            self.language_format = ['he', 'rtl']
            self.booklet_parameters = 'נתוני ספר כיס'
        self.page_header = text[0]
        self.choose_flie_header = text[1]
        self.language_header = text[-2]
        self.inst_pages = text[2]
        self.inst_per_pages = text[3]
        self.inst_merge = text[4]
        self.merge_types = [text[7], text[8]]
        self.page_type_title = text[9]
        self.submit_text = text[10]
    


def find_new_pdf(original_name):
    original_name_part = original_name.split('.')[0]
    list_dir = os.listdir(str(os.getcwd()) + '\\src\\user_files\\')  # get the original and other new file
    files = [file for file in list_dir if original_name_part in file and original_name!=file]
    return files[0]   # should be only one element...

def delete_files(original_name):
    original_name_part = original_name.split('.')[0]
    list_dir = os.listdir(str(os.getcwd()) + '\\src\\user_files\\')  # get the original and other new file
    files = [file for file in list_dir if original_name_part in file]
    for file in files:
        os.remove(str(os.getcwd()) + '\\src\\user_files\\'+file)


def WEB_UI():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def main_url():
        return redirect("/he/")
    
    @app.route("/<string:language>/", methods=['GET', 'POST'])
    def main_site_page(language):
        pages_type = ['A4', 'A5', 'A6', 'A7']
        book_languages = ['עברית', 'English']
        if language=='he':
            form_text = PdfFormText('hebrew')
        else:
            form_text = PdfFormText('english')
        merge_types = form_text.merge_types
        form_data = PdfFormQuestions(pages_type, merge_types, book_languages)
        return render_template("main.html", Title="sifrei_kis", form_data=form_data, form_text=form_text)


    @app.route('/download', methods=['GET', 'POST'])  # download only page doesn't really open any window
    def download():
        user_files = str(os.getcwd()) + '\\src\\user_files\\'
        if request.method == 'POST':
            pdf_file = request.files['file']
            pdf_file.save(user_files + pdf_file.filename)  # physically saves the file at current path of python!
            try:
                number_of_pages_booklet = int(request.form['pages'])
            except:
                print('error in number of pages')
            try:
                number_of_pages_sheet = int(request.form['pages_per_sheet'])
            except:
                print('error in number of pages per sheet')
            merge_type = request.form['pdf_merge_type']
            page_type = request.form['page_size']
            language = request.form['book_lang']

            if merge_type == 'gluing':
                GS_b = True
            else:
                GS_b = False
            
            if language=='עברית':
                language_on = True
            else:
                language_on = False
            # create the new pdf
            # inputs = [values[0], values[1], values[2], '' if GS_b else 's', 'v', 0 if language_on else 1]
            inputs = [user_files + pdf_file.filename, number_of_pages_booklet, number_of_pages_sheet,
                       '' if GS_b else 's', 'v', 0 if language_on else 1]
            making_the_pdf(inputs, eng=0, pNumber=False, cutLines=True)
            
            fileName = find_new_pdf(pdf_file.filename)
            with open(user_files + fileName, "rb") as fh:
                buf = BytesIO(fh.read())
            delete_files(pdf_file.filename)  #delete all files...  assuming no other pdf with the same name
        return send_file(buf, as_attachment=True, mimetype="text/plain", download_name=fileName)

    # 192.168.154.195  port=5000, debug=True
    app.run(host="192.168.154.195", port=8000, debug=True)
    # app.run(host="127.0.0.1", port=8000, debug=True)


if __name__ == '__main__':
    WEB_UI()
