import os
from uuid import uuid4
from datetime import datetime
import csv
from dataclasses import dataclass

from io import BytesIO
from pocket_book import making_the_pdf
from flask import Flask, render_template, request, redirect, send_file, url_for
from pathlib import Path


class Self_page:
    def __init__(self, function_name, language):
        self.self_function=function_name
        self.self_lang=language

class PdfFormQuestions:
    def __init__(self, page_types, merge_types, book_languages):
        self.page_types = page_types
        self.merge_types = merge_types
        self.book_languages = book_languages

@dataclass
class Book:
    filename: str
    timestamp: str
    name: str
    author: str
    language: str
    genre: str
    era: str
    pages_per_sheet: int


ENGLISH_TEXT = [
    "Booklet Project",
    "Choose a file",
    "Enter the number of pages in each booklet (In multiples of 4. the standard is 32): ",
    "Enter the number of pages per sheet (2/4/8/16): ",
    "Sewing or gluing? In the gluing there is an extra blank page on each side.",
    "Gluing",
    "Sewing",
    "Page type",
    "Create Booklet",
    "Hebrew",
    "English",
    "Book's language",
    "Booklet options",
    "Add cut lines?",
    "Add page numbering?",
    "Can we save the result PDF for other user?",
    "Contributing Book",
    "Book's Name",
    "Author's Name",
    "Book's Era",
    "Book's Genre"
]

HEBREW_TEXT = [
    "פרויקט ספרי כיס",
    "בחר קובץ",
    "הכנס את מספר העמודים בכל מחברת (בכפולות של 4, הסטנדרט הוא 32)",
    "הכנס מספר עמודים לעמוד (2/4/8/16)",# todo: בחר גודל רצוי עבור הספר (a5,a6,a7,a8)
    "מודבק או תפור? בגרסא המודבקת יש תוספת של עמוד ריק בכל מחברת",
    "מודבק",
    "תפור",
    "סוג עמוד",
    "צור ספר כיס",
    "עברית",
    "אנגלית",
    "באיזו שפה הספר?",
    "אופציות הדפסה נוספות",
    "האם להוסיף קווי חיתוך?",
    "האם להוסיף מספרי עמודים?",# todo: להוסיף שאלה האם מספרי העמודים יהיו בספרות או באותיות(האותיות רק בעברית)
    "האם אנחנו יכולים להציע את הספרון לעוד משתמשים?",
    "הוספת ספר למאגר",
    "שם הספר",
    "שם המחבר",
    "תקופת הספר",
    "תחום הספר"
]

EN_HOME_TEXT = [
    "Welcome",
    "This is a short about us",
    "Video Title",
    "Create your own PDF Booklet",
    "Community Created Booklets",
    "search books",
]

HE_HOME_TEXT = [
    'ברוכים הבאים',
    'זה הסבר קצר עלינו',
    'סרטון תדמית',
    'ייצר ספרון כיס בעצמך',
    'ספרונים של אחרים',
    'חפש ספרונים'
]

EN_CARDS = [
    'Community Created Booklets',
    'Book\'s / Author\'s Name:',
    "Book's Era",
    "Book's Genre",
    "Author",
    "Language",
    "Genre",
    "Era",
    "Pages per Sheet Recommended",
    'Download!',
    "Search Filters",
    "Hebrew",
    "English"
]

HE_CARDS = [
    'קבצים שיצרו אחרים',
    'שם הספר / המחבר:',
    "תחום הספר",
    "תקופת הספר",
    "מחבר",
    "שפה",
    "תחום",
    "תקופה",
    "מספר מומלץ לעמודים בדף",
    'הורדה!',
    "מסננים",
    "עברית",
    "אנגלית"

]

SFO_OPTIONS = {'eras': ['תנ"ך', 'תנאים', 'אמוראים', 'גאונים', 'ראשונים', 'אחרונים'],
        'genres': ['תנ"ך', 'מקורות תנאיים', 'תלמוד ועיון', 'הלכה', 'מחשבה', 'מוסר', 'מנייני מצוות', 'קבלה', 'חסידות', 'ספרות']}

class PdfFormText:
    # this class is the text container for the web page after language choice
    def __init__(self, language):
        if language == "english":
            text = ENGLISH_TEXT
            self.language_format = ["en", "ltr"]
            self.booklet_parameters = "Booklet parameters"
        else:
            text = HEBREW_TEXT
            self.language_format = ["he", "rtl"]
            self.booklet_parameters = "נתוני ספר כיס"
        self.page_header, self.choose_flie_header = text[0], text[1]
        self.inst_pages, self.inst_per_pages = text[2], text[3]
        self.inst_merge = text[4]
        self.merge_types = [text[5], text[6]]
        self.page_type_title = text[7]
        self.submit_text = text[8]
        self.languges = [text[9], text[10]]
        self.language_header = text[11]
        self.booklet_options = text[12]
        self.cut_lines = text[13]
        self.page_numbering = text[14]

        self.save_for_others = text[15]
        self.sfo_title = text[16]
        self.sfo_book_name = text[17]
        self.sfo_author = text[18]
        self.sfo_genre = text[19]
        self.sfo_era = text[20]

        self.sfo_options = SFO_OPTIONS


def find_new_pdf(original_name):
    original_name_part = Path(original_name).stem
    list_dir = os.listdir('./user_files/')
    files = [file for file in list_dir if original_name_part in file and original_name!=file]
    return files[0]

def delete_files(original_name):
    original_name_part = original_name.split('.')[0]
    list_dir = os.listdir('./user_files/')  # get the original and other new file
    files = [file for file in list_dir if original_name_part in file]
    for file in files:
        os.remove('./user_files/' + file)

DB_PATH = './books_db/'

def get_book_db():
    with open(DB_PATH + 'index.csv', 'r', encoding='utf-8') as index_file:
        # Choosing new name for storting the file (adding uuid to mitigate duplicates)
        reader = csv.reader(index_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)        
        
        reader.__next__() # Skip headers
        books = []
        for row in reader:
            if len(row) == 0: continue # Empty line in csv file

            books.append(Book(*row)) # Unpacks row, can be changed if Book object data isn't identical to index.csv data.

        return books
        

def save_to_db(file, book_name, author, book_lang, era, genre, pages_per_sheet):
    file.seek(0) # After saving once need to seek to start
    with open(DB_PATH + 'index.csv', 'a', encoding='utf-8') as index_file:
        # Choosing new name for storting the file (adding uuid to mitigate duplicates)
        # filename = Path(file.filename).stem + '-' + str(uuid4())[:5] + Path(file.filename).suffix
        filename = book_name + '-' + str(uuid4())[:5] + Path(file.filename).suffix

        file.save(DB_PATH + filename)

        writer = csv.writer(index_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow([filename, datetime.now(), book_name, author, book_lang, era, genre, pages_per_sheet])

def WEB_UI():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def main_url():
        return redirect("/he/home/")
    
    @app.route("/<string:language>/home/", methods=['GET', 'POST'])
    def home(language):
        if language=='he':
            form_text = PdfFormText('hebrew')
            home_text = HE_HOME_TEXT
        else:
            form_text = PdfFormText('english')
            home_text = EN_HOME_TEXT
        page = Self_page('home',language)
        return render_template("home.html", Title="pocket_books_home", 
                               form_text=form_text, home_text=home_text, self_page=page)
    

    @app.route("/<string:language>/past_books/", methods=['GET', 'POST'])
    def past_books(language):
        if request.method == 'POST':
            filename = request.form.get('file_name')
            with open(DB_PATH + filename, "rb") as fh:
                buf = BytesIO(fh.read())
            return send_file(buf, as_attachment=True, mimetype="text/plain", download_name=filename)

        if language=='he':
            form_text = PdfFormText('hebrew')
            cards_text = HE_CARDS
        else:
            form_text = PdfFormText('english')
            cards_text = EN_CARDS

        books = get_book_db()   
        page = Self_page('past_books',language)
        return render_template("past_books.html", Title="past_books_page", 
                               form_text=form_text, cards_text=cards_text, self_page=page,
                               books=books, sfo_options = SFO_OPTIONS)
    
    @app.route("/<string:language>/create_pdf_form", methods=['GET', 'POST'])
    def main_site_page(language):
        if language=='he':
            form_text = PdfFormText('hebrew')
        else:
            form_text = PdfFormText('english')
        merge_types = form_text.merge_types
        book_languages = form_text.languges
        pages_type = ['A4', 'A5', 'A6', 'A7']
        form_data = PdfFormQuestions(pages_type, merge_types, book_languages)
        page = Self_page('main_site_page',language)
        return render_template("full_form.html", Title="pocket_books", form_data=form_data, form_text=form_text, self_page=page)

    @app.route('/download', methods=['GET', 'POST'])  # download - this function doesn't represent any web page
    # it's opening a new tab to download the output file and then closes it.
    def download():
        user_files = './user_files/'
        if request.method == 'POST':
            pdf_file = request.files['file']
            pdf_file.save(user_files + pdf_file.filename)  # physically saves the file at current path of python!
            try:  # recomendeation to use type instead of try. I dont understand who to implement without crash...
                number_of_pages_booklet = int(request.form['pages'])
                number_of_pages_sheet = int(request.form['pages_per_sheet'])
            except:
                print('error in number of pages or in number of pages per sheet')
                return
            
            merge_type = request.form['pdf_merge_type']
            language = request.form['book_lang']
            # future data for usage...
            # page_type = request.form['page_size']
            cut_lines = request.form.get('cut_lines')
            save_for_others = request.form.get('save_for_others')
            if cut_lines == 'cut_lines':
                cut_lines_bool = True
            else:
                cut_lines_bool = False
            
            page_numbering = request.form.get('page_numbering')
            if page_numbering == 'page_numbering':
                page_numbering_bool = True
            else:
                page_numbering_bool = False

            if merge_type == 'gluing' or merge_type == 'מודבק':
                merge_type_text = ''
            else:
                merge_type_text = 's'
            
            if language=='עברית' or language=='Hebrew':
                language_num = 0
            else:
                language_num = 1
            
            if 1:  # not clear when to use this option... until now only used with 'v' option...
                combine_method = 'v'
            else:
                combine_method = ''  # ?
            
            if save_for_others:
                book_name = request.form.get('sfo_book_name')
                author = request.form.get('sfo_author')
                genre = request.form.get('sfo_genre')
                era = request.form.get('sfo_era')

                pages_per_sheets = number_of_pages_sheet # Using user's pages per sheet choice
                book_lang = language_num # Using user's book's language choice

                # save_to_db(pdf_file, "חוטב עצים ושואב מים", "הרא\"ש קטן", book_lang, "אחרונים", "מוסר", 2)
                save_to_db(pdf_file, book_name, author, book_lang, genre, era, pages_per_sheets)

            # create the new pdf
            inputs = [user_files + pdf_file.filename, number_of_pages_booklet, number_of_pages_sheet,
                       merge_type_text, combine_method, language_num]
            making_the_pdf(inputs, eng=0, page_Numbers=page_numbering_bool, cutLines=cut_lines_bool)
            
            fileName = find_new_pdf(pdf_file.filename)
            with open(user_files + fileName, "rb") as fh:
                buf = BytesIO(fh.read())
            delete_files(pdf_file.filename)  #delete all files...  assuming no other pdf with the same name
        return send_file(buf, as_attachment=True, mimetype="text/plain", download_name=fileName)

    # "192.168.154.195" - example of current IP that might change and required for testing on
    # other devices, "127.0.0.1" - self IP for basic coding
    # debug=True - only before production to make working easy
    
    # app.run(host="192.168.154.195", port=8000, debug=True)
    app.run(host="127.0.0.1", port=8000, debug=True)


if __name__ == '__main__':
    WEB_UI()
    # pass
