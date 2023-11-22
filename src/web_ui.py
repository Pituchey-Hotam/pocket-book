import os
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

class Book:
    def __init__(self, name, description, num_pages, type):
        self.name = name
        self.description = description
        self.num_pages = num_pages
        self.type = type

ENGLISH_TEXT =  [
    "booklet project",
    "Choose a file: ",
    "Enter number of pages in each booklet (In multiples of 4. the standard is 32): ",
    "Enter pages per sheet (2/4/8/16): ",
    "Sewing or gluing? In the gluing there is an extra blank page on each side.",
    "gluing",
    "Sewing",
    "page type",
    "create booklet",
    "Hebrew",
    "English",
    "Book language?",
    "booklet options",
    "add cut lines?",
    "add page numbering?",
    "can we save the resault PDF for other user?"
]

HEBREW_TEXT = [
    "פרויקט ספרי כיס",
    "בחר קובץ",
    "הכנס את מספר העמודים בכל מחברת (בכפולות של 4, הסטנדרט הוא 32)",
    "הכנס מספר עמודים לעמוד (2/4/8/16)",
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
    "האם להוסיף מספרי עמודים?",
    "האם אנחנו יכולים להציע את הספרון לעוד משתמשים?"
]

EN_HOME_TEXT = [
    'welcome',
    'this is a short about us',
    'video title',
    'create your own PDF booklet',
    "other's books",
    'search books'
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
    'others pdf\'s',
    'description',
    'number of pages per booklets',
    'book structere: ',
    'Download'
]

HE_CARDS = [
    'קבצים שיצרו אחרים',
    'תיאור',
    'מספר עמודים בספרון',
    'מבנה הספר',
    'הורדה'
]

class PdfFormText:
    # this class is the text container for the web page after language choice
    def __init__(self, language):
        if language == 'english':
            text = ENGLISH_TEXT
            self.language_format = ['en', 'ltr']
            self.booklet_parameters = 'booklet parameters'
        else:
            text = HEBREW_TEXT
            self.language_format = ['he', 'rtl']
            self.booklet_parameters = 'נתוני ספר כיס'
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


def find_new_pdf(original_name):
    original_name_part = Path(original_name).stem
    list_dir = os.listdir('./src/user_files/')
    files = [file for file in list_dir if original_name_part in file and original_name!=file]
    return files[0]

def delete_files(original_name):
    original_name_part = original_name.split('.')[0]
    list_dir = os.listdir('./src/user_files/')  # get the original and other new file
    files = [file for file in list_dir if original_name_part in file]
    for file in files:
        os.remove('./src/user_files/' + file)


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
    @app.route("/<string:language>/past_books/<string:search>/", methods=['GET', 'POST'])
    def past_books(language, search='no_filter'):
        try:
            search = request.form['part_name']
            return redirect('past_books', language=language, search='no_filter')
        except:
            pass
        if language=='he':
            form_text = PdfFormText('hebrew')
            cards_text = HE_CARDS
            search_by_lang= 'חפש'
        else:
            form_text = PdfFormText('english')
            cards_text = EN_CARDS
            search_by_lang='search'
        book1 = Book('תהילים', 'ספרוני תהילים', '32', 'sewing')
        book2 = Book('harav Noah', 'boaring lessons', '4', 'sewing')
        book3 = Book('שיעורי הרב מסתלבט', 'קולות לכל אירוע', '32', 'gluing')
        books = [book1, book2, book3]
        page = Self_page('past_books',language)
        return render_template("past_books.html", Title="past_books_page", 
                               form_text=form_text, cards_text=cards_text, self_page=page,
                               books=books, search_text=search, search_lang=search_by_lang)
    
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
        user_files = './src/user_files/'
        if request.method == 'POST':
            pdf_file = request.files['file']
            pdf_file.save(user_files + pdf_file.filename)  # physically saves the file at current path of python!
            try:  # recomendeation to use type instead of try. I dont understand who to implement without crash...
                number_of_pages_booklet = int(request.form['pages'])
                number_of_pages_sheet = int(request.form['pages_per_sheet'])
            except:
                print('error in number of pages or in number of pages per sheet')
            
            merge_type = request.form['pdf_merge_type']
            language = request.form['book_lang']
            # future data for usage...
            page_type = request.form['page_size']
            cut_lines = request.form.get('cut_lines')
            if cut_lines == 'cut_lines':
                cut_lines_bool = True
            else:
                cut_lines_bool = False
            
            page_numbering = request.form.get('page_numbering')
            if page_numbering == 'page_numbering':
                page_numbering_bool = True
            else:
                page_numbering_bool = False

            if merge_type == 'gluing':
                merge_type_text = ''
            else:
                merge_type_text = 's'
            
            if language=='עברית':
                language_num = 0
            else:
                language_num = 1
            
            if 1:  # not clear when to use this option... until now only used with 'v' option...
                combine_method = 'v'
            else:
                combine_method = ''  # ?
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
