from PySimpleGUI import theme, Button, Text, Input, InputText, FilesBrowse, Window, WIN_CLOSED, Image as guiImage


# Version - important
currentVersion = "2.1.2"

# --------------
#     ♥ UI ♥
# ---------------

ENGLISH_T = [
    "Choose a file: ",
    "Enter number of pages in each booklet (In multiples of 4. the standart is 32): ",
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
              [Button(Langughe[10], size=(6, 1), button_color='white on green', key='-langughe-'),
               Text(Langughe[12], key="L5")],
              [Button(Langughe[13], key="Submit")]]


    # Building Window
    window = Window(Langughe[5], layout, size=(800, 250))

    oneNote_on = True
    GS_b = True
    langughe_on = True
    # graphic_off = True

    while True:
        event, values = window.read()
        if event == WIN_CLOSED or event == "Exit":
            quit()
            break
        elif event == "change":
            Langughe = HEBREW_T if lan == "English" else ENGLISH_T
            lan = "English" if lan != "English" else "עברית"

            window["L0"].update(value=Langughe[0])
            window["L1"].update(value=Langughe[1])
            window["L2"].update(value=Langughe[2])
            window["L3"].update(value=Langughe[3])
            window["L5"].update(value=Langughe[12])
            window["Submit"].update(text=Langughe[13])
            window['-gs-'].update(text=Langughe[6] if GS_b else Langughe[7])
            window['-langughe-'].update(text=Langughe[10] if langughe_on else Langughe[11])
            window['change'].update(text=lan)


        elif event == "Submit":
            break
        elif event == '-gs-':  # if the normal button that changes color and text
            GS_b = not GS_b
            window['-gs-'].update(text=Langughe[6] if GS_b else Langughe[7],
                                  button_color='white on green' if GS_b else 'white on red')
        elif event == '-langughe-':  # if the normal button that changes color and text
            langughe_on = not langughe_on
            window['-langughe-'].update(text=Langughe[10] if langughe_on else Langughe[11],
                                        button_color='white on green' if langughe_on else 'white on red')


    window.close()
    return [values[0], values[1], values[2], '' if GS_b else 's', 'v', 0 if langughe_on else 1]
