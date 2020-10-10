import json
import os
import tkinter
import tkinter.messagebox
from collections import Counter
from os import path
from tkinter import *
from tkinter import ttk

import numpy as np
import pyautogui

pyautogui.FAILSAFE = True
running = False
dict_path = os.getenv('APPDATA') + '\\Markov_Dictionaries\\'
data_location = (os.path.abspath(os.path.dirname(sys.argv[0]))) + "\\Source Data\\"
word_dict = 'Null'
text = 'Null'

# <editor-fold desc="Making the GUI">
window = tkinter.Tk()
window.title = "Word Sender"
window.geometry('400x100')
try:
    v1 = tkinter.PhotoImage(file='icon.png')
    window.iconphoto(False, v1)
except:
    pass
label = ttk.Label(window,
                  text="To Use: Select File from dropdown menu.\nPress the button when you're ready.\nThere will be a 2 second delay before the script starts.",
                  font=('Times New Roman', 13))
label.pack(anchor='nw', side='top')
btn1 = tkinter.Button(window, text="Start the Script!", font=('Times New Roman', 13))
btn1.pack(side=tkinter.LEFT, padx=2)
file_chooser_combobox = ttk.Combobox(window)
file_chooser_combobox.config(exportselection='true', justify='left', values=os.listdir(data_location))
file_chooser_combobox.pack(side=LEFT, fill=BOTH, expand=1, pady=5)  # pack option 2
btn2 = tkinter.Button(window, text="Stop the Script!", font=('Times New Roman', 13))
btn2.pack(side=tkinter.RIGHT, padx=2)


# </editor-fold>

def start():
    global running
    global word_dict
    global text
    global window
    global dict_path
    global data_location
    running = True
    try:
        if file_chooser_combobox.current() == -1:
            text_path = (data_location + (np.random.choice(os.listdir(data_location))))
        else:
            text_path = (data_location + (os.listdir(data_location))[file_chooser_combobox.current()])
    except ValueError:
        tkinter.messagebox.showerror(title="No files found",
                                     message="The folder that should contain the source text files contains nothing.\n Move some source text files to " + data_location + " and try to run the program again.")
    try:
        text = open(text_path).read()
    except UnicodeDecodeError:
        tkinter.messagebox.showerror(title="Bad Characters in the source Document",
                                     message="An unprocessable character was found in the selected document.\n"
                                             "This is usually caused by non-ASCII characters in the file if the selected file is a text file,  or by an invalid file type, such as an image.\n"
                                             "Try another file or attempt to remove the bad characters.")
        running = False
        main()
    word_dict = get_dict(text_path)
    go()


def stop():
    global running
    running = False


def make_pairs(text_local):
    text_local = text_local.split()
    for i in range(len(text_local) - 1):
        yield text_local[i], text_local[i + 1]


def make_dict(pairs):
    word_dict_local = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict_local.keys():
            word_dict_local[word_1].append(word_2)
        else:
            word_dict_local[word_1] = [word_2]
    return word_dict_local


def make_model(text_local):
    pairs = make_pairs(text_local)
    word_dict_local = make_dict(pairs)
    return word_dict_local


def get_dict(text_file):
    # try:
    global dict_path
    json_file_name = 'dict_' + os.path.splitext(os.path.basename(text_file))[0] + '.json'
    json_file_path = dict_path + json_file_name
    if not os.path.exists(dict_path):
        os.makedirs(dict_path)
    if path.exists(json_file_path):
        with open(json_file_path) as json_file_path:
            word_dict_local = json.load(json_file_path)
    else:
        word_dict_local = make_model(open(text_file).read())
        with open(json_file_path, 'w') as outfile:
            json.dump(word_dict_local, outfile)
    # except:
    #     tkinter.messagebox.showwarning(title="Bad thing happened", message="Something very bad happened while getting or making the dictionary file."
    #                                                                        "\nTry manually deleting the dictionary files, then running the program again."
    #                                                                        "\n\tThe dictionary files are found at %appdata%\\Markov_Dictionaries.")
    #     sys.exit(0)
    return word_dict_local


def generate_text(first_word, word_dict_local, text_local):
    if first_word == 'NullNull':
        chain = [np.random.choice(text_local.split())]
    else:
        chain = [first_word]
    try:
        while True:
            curr_word = np.random.choice(word_dict_local[chain[-1]])
            chain.append(curr_word)
            if any(x in curr_word for x in ('!', '?', '.', "-\n")) and not any(
                    x in curr_word for x in ('Mr.', 'Ms.', 'Mrs.')):
                return chain
    except:
        tkinter.messagebox.showerror(title="Fatal error",
                                     message="Word not found in dictionary.\nRun the program again.")


def remove_duplicates(lst):
    dropped_indices = set()
    counter = Counter(tuple(lst[i:i + 2]) for i in range(len(lst) - 1))

    for i in range(len(lst) - 2, -1, -1):
        sub = tuple(lst[i:i + 2])
        if counter[sub] > 1:
            dropped_indices |= {i, i + 1}
            counter[sub] -= 1
    return [x for i, x in enumerate(lst) if i not in dropped_indices]


def cleanup(output_text):
    output_text = " ".join(remove_duplicates(output_text))
    output_text = output_text[0:2].capitalize() + output_text[2:]
    return output_text


def go():
    global word_dict
    global text
    global running
    global window
    if running:
        output = cleanup(generate_text('NullNull', word_dict, text))
        pyautogui.typewrite(output, interval=0.01)
        pyautogui.press('enter')
        window.after(500, go)


def main():
    try:
        if not os.path.exists(data_location):
            os.makedirs(data_location)
        btn1.config(command=lambda: start())
        btn2.config(command=stop)
        window.after(500, go)
        window.mainloop()
    except:
        tkinter.messagebox.showerror(title="Something Happened",
                                     message="Something very bad happened, and I have no clue what that something could be.\n"
                                             "You could try:\n\t"
                                             "1) Restarting the program\n\t"
                                             "2) Making sure that the file you selected is a .txt file\n\t"
                                             "3) Making sure that all the characters in the source document are valid ASCII characters.")


if __name__ == "__main__":
    main()
