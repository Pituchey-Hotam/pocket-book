from pdfbooklet_new import *
from ui_settings import *
from pdf_to_tiny_book_2_1_2 import *

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file


class PdfFormQuestions:
    def __init__(self, page_types, merge_types, book_languages):
        self.page_types = page_types
        self.merge_types = merge_types
        self.book_languages = book_languages


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main_site_page():
    pages_type = ['A4', 'A5', 'A6', 'A7']
    merge_types = ['gluing', 'sewing']
    book_languages = ['עברית', 'English']
    form_data = PdfFormQuestions(pages_type, merge_types, book_languages)
    return render_template("main.html", Title="sifrei_kis", form_data=form_data)


@app.route('/download', methods=['GET', 'POST'])  # download
def download():
    user_files = './user_files/'
    if request.method == 'POST':
        # get pdf file
        pdf_file = request.files['file']
        pdf_file.save(user_files + pdf_file.filename)  # physically saves the file at current path of python!
        # get number of pages
        try:
            number_of_pages_booklet = int(request.form['pages'])
        except:
            print('error in number of pages')
        try:
            number_of_pages_sheet = int(request.form['pages_per_sheet'])
        except:
            print('error in number of pages per sheet')
        # get merge type
        merge_type = request.form['pdf_merge_type']
        # get page type
        page_type = request.form['page_size']
        # create the new pdf

        # making_the_pdf_online_version()
        # send_file('king of kosh.png', as_attachment=True)
    return send_file('king of kosh.png', as_attachment=True)


def main():
    app.run(host="127.0.0.1", port=8000, debug=True)


if __name__ == '__main__':
    main()
