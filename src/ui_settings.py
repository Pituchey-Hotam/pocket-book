from PySimpleGUI import theme, Button, Text, Input, InputText, FilesBrowse, Window, WIN_CLOSED, Image as guiImage

# --------------
#     ♥ UI ♥
# ---------------


# this function get folder and check if it including pictures file (and return the names of the pictures and how much
# picture have)
def UI():
    theme("DarkTeal2")
    Language = ENGLISH_T
    lan = "English"
    layout = [[Button("English", key="change")],
              [Text(Language[0], key="L0"), Input(), FilesBrowse(key=0)],
              [Text(Language[1], key="L1"), InputText()],
              [Text(Language[2], key="L2"), InputText()],
              [Button(Language[6], size=(6, 1), button_color='white on green', key='-gs-'),
               Text(Language[3], key="L3")],
              [Button(Language[10], size=(6, 1), button_color='white on green', key='-language-'),
               Text(Language[12], key="L5")],
              [Button(Language[13], key="Submit")]]

    # Building Window
    window = Window(Language[5], layout, size=(800, 250))

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
            window['-language-'].update(text=Language[10] if language_on else Language[11])
            window['change'].update(text=lan)

        elif event == "Submit":
            break
        elif event == '-gs-':  # if the normal button that changes color and text
            GS_b = not GS_b
            window['-gs-'].update(text=Language[6] if GS_b else Language[7],
                                  button_color='white on green' if GS_b else 'white on red')
        elif event == '-language-':  # if the normal button that changes color and text
            language_on = not language_on
            window['-language-'].update(text=Language[10] if language_on else Language[11],
                                        button_color='white on green' if language_on else 'white on red')

    window.close()
    return [values[0], values[1], values[2], '' if GS_b else 's', 'v', 0 if language_on else 1]
