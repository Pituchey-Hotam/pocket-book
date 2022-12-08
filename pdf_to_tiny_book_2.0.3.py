import os
from os import mkdir
from os.path import exists
from shutil import rmtree
from math import ceil

import requests
from PyPDF2 import PdfFileReader, PdfFileWriter
from PySimpleGUI import theme, Button, Text, Input, InputText, FilesBrowse, Window, WIN_CLOSED

from PIL import Image
from time import sleep

import pdfbooklet_new

from random import choice

# Version - important
currentVersion = "2.0.3"


# --------------
#     ♥ UI ♥
#---------------

ENGLISH_T = [
    "Choose a file: ",
    "Enter number of pages in each booklet (In multiples of 4. the standart is 32): ",
    "Enter pages per sheet (2/4/8/16): ",
    "Sewing or gluing? In the gluing there is an extra blank page on each side.",
    "only one notebook?",
    "Gimdany's mini books maker " + currentVersion,
    "gluing",
    "Sewing",
    "Yes",
    "No",
    "Do it"
]

HEBREW_T = [
    "בחר קובץ",
    "הכנס את מספר העמודים בכל מחברת (בכפולות של 4, הסטנדרט הוא 32)",
    "הכנס מספר עמודים לעמוד (2/4/8/16)",
    "מודבק או תפור? בגרסא המודבקת יש תוספת של עמוד ריק בכל מחברת",
    "האם כבודו מדפיס רק מחברת אחת?",
    "יוצר הספרונים של דביר ומלאכי" + currentVersion,
    "מודבק",
    "תפור",
    "כן",
    "לא",
    "יאללה לעבודה"
]

# this function get folder and check if it including pictures file (and return the names of the pictures and how much
# picture have)
def UI():
    
    theme("DarkTeal2")
    Langughe = ENGLISH_T
    lan = "English"
    layout = [[Button("English", key="change")],
              [Text(Langughe[0], key="L0"), Input(), FilesBrowse(key=0)],
              [Text(Langughe[1], key="L1"), InputText()],
              [Text(Langughe[2], key="L2"), InputText()],
              [Button(Langughe[6], size=(6, 1), button_color='white on green', key='-gs-'),
               Text(Langughe[3], key="L3")],
              [Button(Langughe[9], size=(3, 1), button_color='white on green', key='-oneNote-'),
               Text(Langughe[4], key="L4")],
              [Button(Langughe[10], key="Submit")]]
    #              [sg.Button('', image_data=toggle_btn_off, key='-TOGGLE-GRAPHIC-', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)]]

    # Building Window
    window = Window(Langughe[5], layout, size=(800, 250))
    oneNote_on = True
    GS_b = True
    # graphic_off = True

    while True:
        event, values = window.read()
        if event == WIN_CLOSED or event == "Exit":
            break
        elif event == "change":
            Langughe = HEBREW_T if lan == "English" else ENGLISH_T
            lan = "English" if lan != "English" else "עברית"

            window["L0"].update(value=Langughe[0])
            window["L1"].update(value=Langughe[1])
            window["L2"].update(value=Langughe[2])
            window["L3"].update(value=Langughe[3])
            window["L4"].update(value=Langughe[4])
            window["Submit"].update(text=Langughe[10])
            window['-oneNote-'].update(text=Langughe[9] if oneNote_on else Langughe[8])
            window['-gs-'].update(text=Langughe[6] if GS_b else Langughe[7])
            window['change'].update(text=lan)

        elif event == "Submit":
            break
        elif event == '-oneNote-':  # if the normal button that changes color and text
            oneNote_on = not oneNote_on
            window['-oneNote-'].update(text=Langughe[9] if oneNote_on else Langughe[8],
                                       button_color='white on green' if oneNote_on else 'white on red')
        elif event == '-gs-':  # if the normal button that changes color and text
            GS_b = not GS_b
            window['-gs-'].update(text=Langughe[6] if GS_b else Langughe[7],
                                  button_color='white on green' if GS_b else 'white on red')
        """elif event == '-TOGGLE-GRAPHIC-':  # if the graphical button that changes images
            graphic_off = not graphic_off
            window['-TOGGLE-GRAPHIC-'].update(image_data=toggle_btn_off if graphic_off else toggle_btn_on)"""

    window.close()
    return [values[0], values[1], values[2], '' if GS_b else 's', 'v' if oneNote_on else '']


# -----------------------
#     pdf manipulation
#------------------------

def extract_num_of_pages(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
    f.close()
    return number_of_pages


def split(path, name_of_split, sp, length, bind_method='s'):
    # length += (4-(length%4))*(length%4 > 0)
    pdf = PdfFileReader(path)
    output = f'{name_of_split}'
    pdf_writer = PdfFileWriter()

    for page in range(sp, sp + length):
        if page < pdf.getNumPages():
            pdf_writer.addPage(pdf.getPage(page))
        else:
            pdf_writer.addBlankPage()
    if not bind_method == 's':
        pdf_writer.insertBlankPage(0)
        pdf_writer.addBlankPage()

    with open(output, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    output_pdf.close()


def split_Even_Odd(path, name_of_split):
    pdf = PdfFileReader(path)
    output_ev = f'{name_of_split}_even.pdf'
    output_odd = f'{name_of_split}_odd.pdf'
    pdf_writer_ev = PdfFileWriter()
    pdf_writer_odd = PdfFileWriter()
    number_of_pages = extract_num_of_pages(path)
    number_of_pages_plusblank = int((4 - (number_of_pages / 2 % 4)) * (number_of_pages / 2 % 4 > 0))
    for page in range(number_of_pages + number_of_pages_plusblank):
        if page < number_of_pages:
            if page % 2 == 0:
                pdf_writer_odd.addPage(pdf.getPage(page))
            else:
                pdf_writer_ev.addPage(pdf.getPage(page))
        else:
            pdf_writer_ev.addBlankPage()
            pdf_writer_odd.addBlankPage()

    with open(output_ev, 'wb') as output_pdf:
        pdf_writer_ev.write(output_pdf)
    output_pdf.close()
    with open(output_odd, 'wb') as output_pdf:
        pdf_writer_odd.write(output_pdf)
    output_pdf.close()


def rotate(path, name_of_rotate, num_rot=3):
    pdf = PdfFileReader(path)
    number_of_pages = extract_num_of_pages(path)
    output = f'{name_of_rotate}'
    pdf_writer = PdfFileWriter()
    for page in range(number_of_pages):
        page_1 = pdf.getPage(page).rotateClockwise(90 * num_rot)
        pdf_writer.addPage(page_1)

    with open(output, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    output_pdf.close()


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)
    out.close()


def merge_sort_pdfs(path1, path2, output):
    pdf_writer = PdfFileWriter()
    pdf1 = PdfFileReader(path1)
    pdf2 = PdfFileReader(path2)
    number_of_pages = extract_num_of_pages(path1)
    for page in range(number_of_pages):
        pdf_writer.addPage(pdf1.getPage(page))
        pdf_writer.addPage(pdf2.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)
    out.close()


def pile_combine(file, path, file_name):
    tmp_num = extract_num_of_pages(file)
    split(file, path + file_name + 's1.pdf', 0, ceil(tmp_num / 2))
    split(file, path + file_name + 's2.pdf', ceil(tmp_num / 2), tmp_num)

    merge_sort_pdfs(path + file_name + 's1.pdf', path + file_name + 's2.pdf', file)


#--------------------------------
#    Upgrade code (very cool☺)
#---------------------------------
def UPGRADE():
    data = currentVersion

    p = "\\\\YBMSERVER\lessons_files\מחזור מה\תיקיות תלמידים\דביר ג'מדני\לא לגעת\Version.txt"
    if exists(p):
        a = open(p, 'r')
        data = a.readline()
        a.close()
        location = "\"\\\\YBMSERVER\lessons_files\מחזור מה\תיקיות תלמידים\דביר ג'מדני\לא לגעת\pdf_to_tiny_book_"
        # הרווחים עושים בעיות
        command = '''xcopy %2 .\ /Y'''
        print('version from file: ' + data)
        print(location)
    else:
        try:
            URL = requests.get('https://raw.githubusercontent.com/gimdani/pdf-to-tiny-book/main/Version.txt',
                               verify=False, timeout=2)
            data = URL.text
            location = "\"https://raw.githubusercontent.com/gimdani/pdf-to-tiny-book/main/pdf_to_tiny_book_"
            command = '''curl %2 -o ''' + "pdf_to_tiny_book_" + str(data) + ".exe"
            command = command.replace("\n", "")            
            print('version from git: ' + data)
        except:
            print("cannot find connection to upgrades base")

    if (int((str(data).replace("\n",'')).replace(".",'')) <= int(currentVersion.replace(".",''))):
        print("App is up to date!")
        if os.path.exists("update.bat"):
            os.remove("update.bat")

    else:
        ok = False
        win_update_layout = [[Text(
            "App is not up to date! App is on version " + currentVersion + " but could be on version " + str(
                data) + "!")],
            [Text("Do the update?")],
            [Button(button_text="OK", key="-ok-"), Button(button_text="ask me later", key="-no-")]]
        window_up = Window("upgrade" + data, win_update_layout, size=(500, 100), modal=True)
        while True:
            event, values = window_up.read()
            if event == WIN_CLOSED or event == "-no-":
                break
            elif event == "-ok-":
                ok = True
                break
        window_up.close()

        # print("App is not up to date! App is on version " + currentVersion + " but could be on version " + str(data) + "!")

        if ok:
            update = open(r'update.bat', 'w+')
            s = '''ping 127.0.0.1 -n 2 > nul
                        del %1
                        ::ping 127.0.0.1 -n 6 > nul
                        ''' + command + '''
                        start "" %3
                        exit'''
            update.write(s)
            update.close()
            cmd = "start cmd /c update.bat \"pdf_to_tiny_book_" + currentVersion + ".exe\" " + location + data + ".exe\" pdf_to_tiny_book_" + str(data) + ".exe"
            cmd = cmd.replace("\n", '')
            print(cmd)
            os.system(cmd)
            print("hii")
            # time.sleep(5)

            quit()

#----------------------------
#   Advertise (super cool☻)
#-----------------------------

def Advertise():
    p = "\\\\YBMSERVER\lessons_files\מחזור מה\תיקיות תלמידים\דביר ג'מדני\פרסומות"
    if exists(p):
        sleep(1.5)
        im = Image.open(p + '\\'+ choice(os.listdir(p)))
        im.show('image',im)
        print(im)


#~~~~~~~~~~~~~~~~~
#     main ♪♫♪
#~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    
    UPGRADE() # upgrade the code
    # Thread(target=UPGRADE).start()

    win_load_layout = [[Text(text="making your file")],
                       [Text(text="this may take a few minutes")]]
    window_load = Window("please wait", win_load_layout, size=(200, 60))

    inputs = UI() # calling the UI

    while True:
        window_load.read(timeout=10)

        Advertise() # advertising

        inputs[0] = inputs[0].split(';')
        for inp in inputs[0]:
            inp = inp.replace('\\', '/')

            file_name = inp.split('/')[-1]
            old_path = inp[:-len(file_name) - 1] + '/'

            print(old_path)
            print(file_name)

            dir_path = old_path + 'trash ' + file_name[:-4]
            path = dir_path[:] + '\\'  # argv[2]+'\\'
            if not exists(path):
                mkdir(path)

            file = old_path + file_name  # argv[1]+argv[2]+'.pdf'

            notebook_len = int(inputs[1])

            pages_per_sheet = int(inputs[2])
            bind_method = inputs[3]

            combine_method = inputs[4]
            # path=pathlib.Path(__file__).parent.resolve()
            number_of_pages = extract_num_of_pages(file)

            paths = []
            if not bind_method == 's':
                notebook_len -= 2
            for i in range(int(number_of_pages / notebook_len) + (number_of_pages % notebook_len > 0)):
                split(file, path + file_name + str(i + 1) + '.pdf', i * notebook_len, notebook_len, bind_method)
                pdfbooklet_new.pdfbooklet(path + file_name + str(i + 1) + '.pdf',
                                          path + file_name + str(i + 1) + 'let.pdf')
                paths.append(path + file_name + str(i + 1) + 'let.pdf')
            if pages_per_sheet == 2:
                path = old_path
            final_path = path + file_name + '_merged.pdf'
            merge_pdfs(paths, output=final_path)
            if pages_per_sheet > 2:
                split_Even_Odd(final_path, path + file_name)

                rotate(path + file_name + '_odd.pdf', path + file_name + '_odd_rotated.pdf')
                rotate(path + file_name + '_even.pdf', path + file_name + '_even_rotated.pdf')

                if combine_method == 'v':
                    odd_path = path + file_name + '_odd_rotated.pdf'
                    even_path = path + file_name + '_even_rotated.pdf'
                    pile_combine(odd_path, path, file_name)
                    pile_combine(even_path, path, file_name)

                odd_path = path + file_name + '_odd_let.pdf'
                even_path = path + file_name + '_even_let.pdf'
                pdfbooklet_new.pdfbooklet(path + file_name + '_odd_rotated.pdf', odd_path, 1, booklet=0)
                pdfbooklet_new.pdfbooklet(path + file_name + '_even_rotated.pdf', even_path, 1, booklet=0)

                if pages_per_sheet > 4:
                    rotate(odd_path, path + file_name + '_odd_rotated2.pdf')
                    rotate(even_path, path + file_name + '_even_rotated2.pdf', 1)
                    if combine_method == 'v':
                        odd_path = path + file_name + '_odd_rotated2.pdf'
                        even_path = path + file_name + '_even_rotated2.pdf'
                        pile_combine(odd_path, path, file_name)
                        pile_combine(even_path, path, file_name)

                    odd_path = path + file_name + '_odd_let2.pdf'
                    even_path = path + file_name + '_even_let2.pdf'
                    pdfbooklet_new.pdfbooklet(path + file_name + '_odd_rotated2.pdf', odd_path, booklet=0)
                    pdfbooklet_new.pdfbooklet(path + file_name + '_even_rotated2.pdf', even_path, booklet=0, eng=1)

                    if pages_per_sheet > 8:
                        rotate(odd_path, path + file_name + '_odd_rotated3.pdf')
                        rotate(even_path, path + file_name + '_even_rotated3.pdf', 1)
                        if combine_method == 'v':
                            odd_path = path + file_name + '_odd_rotated3.pdf'
                            even_path = path + file_name + '_even_rotated3.pdf'
                            pile_combine(odd_path, path, file_name)
                            pile_combine(even_path, path, file_name)

                        odd_path = path + file_name + '_odd_let3.pdf'
                        even_path = path + file_name + '_even_let3.pdf'
                        pdfbooklet_new.pdfbooklet(path + file_name + '_odd_rotated3.pdf', odd_path, booklet=0)
                        pdfbooklet_new.pdfbooklet(path + file_name + '_even_rotated3.pdf', even_path, booklet=0)

                final_path = old_path + file_name[:-4] + ' ready to print.pdf'
                merge_sort_pdfs(odd_path, even_path, final_path)
            # dir_path = dir_path.replace('/', '\\')
            print(dir_path)
            rmtree(dir_path, ignore_errors=False)
            old_path = old_path.replace('/', '\\')
        break

    window_load.close()

    """ win_end_layout = [[Text(text="your file:")],
                            [Text(text=final_path)],
                            [Text(text="this the same original file directory")]
                            [Button(button_text="quit", key="Exit")]]
            window_load = Window("finish", win_end_layout, size=(500, 90), finalize=True)
            while True:
                event, values = window_load.read()
                if event == WIN_CLOSED or event == "Exit":
                    break

            print("Completed! Book is in " + final_path)"""
