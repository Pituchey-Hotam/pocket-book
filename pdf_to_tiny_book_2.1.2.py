import io
import os
import time
import uuid

from os import mkdir
from os.path import exists
from shutil import rmtree
from math import ceil
from threading import Thread

import requests
from PyPDF2 import PdfFileReader, PdfFileWriter
from PySimpleGUI import theme, Button, Text, Input, InputText, FilesBrowse, Window, WIN_CLOSED, Image as guiImage

from PIL import Image

import pdfbooklet_new

from random import choice

# Version - important
currentVersion = "2.1.2"

# --------------
#     ♥ UI ♥
# ---------------

ENGLISH_T = [
    "Choose a file: ",
    "Enter number of pages in each booklet (In multiples of 4. the standard is 32): ",
    "Enter pages per sheet (2/4/8/16): ",
    "Sewing or gluing? In the gluing there is an extra blank page on each side.",
    "only one notebook?",
    "DG & MM mini books maker " + currentVersion,
    "gluing",
    "Sewing",
    "Yes",
    "No",
    "Hebrew",
    "English",
    "Book language?",
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
    "עברית",
    "אנגלית",
    "באיזו שפה הספר?",
    "יאללה לעבודה"
]


# Gets a folder and check if it including pictures file (and return the names of the pictures and how much
# picture have)
def UI(check_updates=True):
    theme("DarkTeal2")
    Language = ENGLISH_T
    lan = "English"
    layout = [[Button("English", key="change")],
              [Text(Language[0], key="L0"), Input(), FilesBrowse(key=0)],
              [Text(Language[1], key="L1"), InputText()],
              [Text(Language[2], key="L2"), InputText()],
              [Button(Language[6], size=(6, 1), button_color='white on green', key='-gs-'),
               Text(Language[3], key="L3")],
              [Button(Language[10], size=(6, 1), button_color='white on green', key='-Language-'),
               Text(Language[12], key="L5")],
              [Button(Language[13], key="Submit")]]
    #              [sg.Button('', image_data=toggle_btn_off, key='-TOGGLE-GRAPHIC-', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)]]

    # Building Window
    window = Window(Language[5], layout, size=(800, 250))

    if check_updates:
        Thread(target=upgrade_with_event, args=[window]).start()

    oneNote_on = True
    GS_b = True
    language_on = True
    # graphic_off = True

    while True:
        event, values = window.read()
        if event == WIN_CLOSED or event == "Exit":
            quit()
            break
        elif event == "change":
            Language = HEBREW_T if lan == "English" else ENGLISH_T
            lan = "English" if lan != "English" else "עברית"

            window["L0"].update(value=Language[0])
            window["L1"].update(value=Language[1])
            window["L2"].update(value=Language[2])
            window["L3"].update(value=Language[3])
            window["L5"].update(value=Language[12])
            window["Submit"].update(text=Language[13])
            window['-gs-'].update(text=Language[6] if GS_b else Language[7])
            window['-Language-'].update(text=Language[10] if language_on else Language[11])
            window['change'].update(text=lan)


        elif event == "Submit":
            break
        elif event == '-gs-':  # if the normal button that changes color and text
            GS_b = not GS_b
            window['-gs-'].update(text=Language[6] if GS_b else Language[7],
                                  button_color='white on green' if GS_b else 'white on red')
        elif event == '-language-':  # if the normal button that changes color and text
            language_on = not language_on
            window['-Language-'].update(text=Language[10] if language_on else Language[11],
                                        button_color='white on green' if language_on else 'white on red')
        elif event == '-UPGRADE-':
            params = values['-UPGRADE-']
            UpgradeWindow(params[0], params[1], params[2])

    window.close()
    return [values[0], values[1], values[2], '' if GS_b else 's', 'v', 0 if language_on else 1]


# -----------------------
#     pdf manipulation
# ------------------------

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


def pile_combine(file, path):
    tmp_num = extract_num_of_pages(file)
    split(file, path + 's1.pdf', 0, ceil(tmp_num / 2))
    split(file, path + 's2.pdf', ceil(tmp_num / 2), tmp_num)

    merge_sort_pdfs(path + 's1.pdf', path + 's2.pdf', file)


# --------------------------------
#    Upgrade code (very cool☺)
# ---------------------------------
def UpgradeWindow(data, command, location):
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
        cmd = "start cmd /c update.bat \"pdf_to_tiny_book_" + currentVersion + ".exe\" " + location + data + ".exe\" pdf_to_tiny_book_" + str(
            data) + ".exe"
        cmd = cmd.replace("\n", '')
        print(cmd)
        os.system(cmd)
        print("hii")
        # time.sleep(5)

        quit()


def chk_UPGRADE():
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

    if (int((str(data).replace("\n", '')).replace(".", '')) <= int(currentVersion.replace(".", ''))):
        print("App is up to date! version: " +currentVersion)
        if os.path.exists("update.bat"):
            os.remove("update.bat")

    else:
        return [data, command, location]
        UpgradeWindow(data, command, location)
    return None


def upgrade_with_event(window):
    l = chk_UPGRADE()
    if not l:
        return
    else:
        while window.thread_queue is None:
            time.sleep(0.3)
        window.write_event_value('-UPGRADE-', l)


# ----------------------------
#   Advertise (super cool☻)
# -----------------------------

def Advertise(thr):
    S = True
    p = "\\\\YBMSERVER\lessons_files\מחזור מה\תיקיות תלמידים\דביר ג'מדני\פרסומות"

    f1 = ("David", 18)
    f2 = ("David", 14)
    f3 = ("Guttman Rashi", 12)
    elements = [[Text(text="please wait, your file will be ready soon", font=f1)],
                [Text(text="Ads: (you may close this window if you want)", font=f2)],
                [guiImage(key="-IMAGE-")],
                [Text(text="לפרסום תוכן ניתן לפנות לדביר ג'מדני", font=f3)]]
    ads_win = Window("ads", elements, size=(520, 390))

    files = []
    flag = False
    sec = 2900
    if exists(p):
        for f in os.listdir(p):
            if any(f.endswith(ex) for ex in ['jpg', 'jpeg', 'bmp', 'png', 'gif']):
                files.append(f)
        flag = True
        print(os.listdir(p))
        print(files)
    else:
        response = requests.get(
            "https://github.com/gimdani/pdf-to-tiny-book/blob/main/%D7%A4%D7%A8%D7%A1%D7%95%D7%9E%D7%AA.jpg?raw=true")
        # img = Image.open(io.BytesIO(response.content))
        # files.append(response)
        print("Image from github")
    while thr.is_alive():
        event, values = ads_win.read(timeout=100)
        if event == WIN_CLOSED:
            break

        sec += 100
        if sec >= 3000:
            sec -= 3000
            if flag:
                im_loc = p + '\\' + choice(files)
            else:
                im_loc = io.BytesIO(response.content)
            im = Image.open(im_loc)
            # im.show('image', im)
            print(im)
            im.thumbnail((500, 400))
            bio = io.BytesIO()
            im.save(bio, format="PNG")
            ads_win["-IMAGE-"].update(data=bio.getvalue())

    ads_win.close()


# ~~~~~~~~~~~~~~~~~
#     the final pdf maker ♪♫♪
# ~~~~~~~~~~~~~~~~~
def combineMethod(trash_file, num):
    odd_path = trash_file + '_odd_rotated' + num + '.pdf'
    even_path = trash_file + '_even_rotated' + num + '.pdf'
    pile_combine(odd_path, trash_file)
    pile_combine(even_path, trash_file)


def moreThan(trash_file, combine_method, eng, num=1):
    n = str(num)
    pev = str(num-1)
    if pev == '0':
        pev = ''

    odd_path = trash_file + '_odd' + pev + '.pdf'
    even_path = trash_file + '_even' + pev + '.pdf'

    rotate(odd_path, trash_file + '_odd_rotated' + n + '.pdf')
    rotate(even_path, trash_file + '_even_rotated' + n + '.pdf')

    if combine_method == 'v':
        combineMethod(trash_file, n)

    odd_path = trash_file + '_odd' + n + '.pdf'
    even_path = trash_file + '_even' + n + '.pdf'

    pdfbooklet_new.pdfbooklet(trash_file + '_odd_rotated' + n + '.pdf', odd_path, booklet=0, eng=eng)
    if num % 2 == 0:
        eng = (eng == 0)
    pdfbooklet_new.pdfbooklet(trash_file + '_even_rotated' + n + '.pdf', even_path, booklet=0, eng=eng)

    return odd_path, even_path


def making_the_pdf(inputs, eng=0):
    inputs[0] = inputs[0].split(';')
    for inp in inputs[0]:
        inp = inp.replace('\\', '/')

        file_name = inp.split('/')[-1]
        old_path = inp[:-len(file_name) - 1] + '/'

        dir_path = old_path + 'trash ' + file_name[:-4]
        path = dir_path[:] + '\\'  # argv[2]+'\\'
        if not exists(path):
            mkdir(path)

        file = old_path + file_name  # argv[1]+argv[2]+'.pdf'
        trash_file = path + file_name

        notebook_len = int(inputs[1])
        pages_per_sheet = int(inputs[2])
        bind_method = inputs[3]
        combine_method = inputs[4]
        eng = inputs[5]
        number_of_pages = extract_num_of_pages(file)

        paths = []
        if not bind_method == 's':
            notebook_len -= 2
        for i in range(int(number_of_pages / notebook_len) + (number_of_pages % notebook_len > 0)):
            name_trash_file = trash_file + str(i + 1)
            split(file, name_trash_file + '.pdf', i * notebook_len, notebook_len, bind_method)
            pdfbooklet_new.pdfbooklet(name_trash_file + '.pdf', name_trash_file + 'let.pdf', eng=eng)
            paths.append(name_trash_file + 'let.pdf')
        if pages_per_sheet == 2:
            path = old_path
            trash_file = path + file_name
        final_path = trash_file + '_merged.pdf'
        merge_pdfs(paths, output=final_path)

        if pages_per_sheet > 2:
            split_Even_Odd(final_path, trash_file)

            counter = 1
            while pages_per_sheet/(counter**2) > 1:
                print(pages_per_sheet/(counter**2))
                print(counter)
                odd_path, even_path = moreThan(trash_file, combine_method, eng, counter)
                counter += 1

            final_path = old_path + file_name[:-4] + ' ready to print.pdf'
            merge_sort_pdfs(odd_path, even_path, final_path)

        rmtree(dir_path, ignore_errors=False)


# ~~~~~~~~~~~~~~~~~
#   checking users
# ~~~~~~~~~~~~~~~~~
def check_user():
    p = "\\\\YBMSERVER\\lessons_files\\מחזור מו\\תיקיות תלמידים\\מלאכי מחפוד\\לא לגעת\\users.txt"

    if not exists(p):
        return ''

    with open(p, 'r') as macs_addrs:
        exist = False
        Lines = macs_addrs.readlines()
        # print(Lines)
        for line in Lines:
            # print(line.strip())
            if line.strip() == str(uuid.getnode()):
                exist = True
                break

    if not exist:
        with open(p, 'a+') as macs_addrs:
            macs_addrs.write(str(uuid.getnode()) + "\n")


# ~~~~~~~~~~~~~~~~~
#     main ♪♫♪
# ~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    # Advertise()  # advertising

    # upgrade_with_event()
    # UPGRADE()  # upgrade the code
    # thU = Thread(target=UPGRADE)
    # thU.start()
    # inputs = UI(thU)
    # Thread(target=UPGRADE).start()
    updates = start = True
    while start:
        inputs = UI(updates)  # calling the UI
        updates = start = False
        # window_load.read(timeout=10)

        # Advertise()  # advertising

        th = Thread(target=making_the_pdf, args=[inputs, 1])
        th.start()

        Advertise(th)
        check_user()  # something evil

        while th.is_alive():
            pass

        win_end_layout = [[Text(text="your file is ready")],
                          [Text(text="have a nice day")],
                          [Button(button_text="Home page", key='-again-')]]
        window_end = Window("thank U", win_end_layout, size=(200, 100))

        while True:
            event, values = window_end.read()
            if event == WIN_CLOSED:
                break
            if event == '-again-':
                start = True
                break
        window_end.close()
