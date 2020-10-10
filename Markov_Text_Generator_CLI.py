import json
import os
import time
from collections import Counter
from os import path

import numpy as np
import pyautogui


# TODO: Make this a class with constructor.
# TODO: Make the program only open the dictionary once.
# TODO: Add the Dictionary location as an optional argument
# TODO: Make the first_word an optional argument
# TODO: Remove main() from this class
# TODO: Remove all the methods made for the CLI, put them in their own class.
# TODO: Make a GUI

def make_pairs(text):
    text = text.split()
    for i in range(len(text) - 1):
        yield text[i], text[i + 1]

def make_dict(pairs):
    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]
    return word_dict

def make_model(text):
    pairs = make_pairs(text)
    word_dict = make_dict(pairs)
    return word_dict

def generate_text(first_word, word_dict, text):
    if first_word == 'NullNull':
        chain = [np.random.choice(text.split())]
    else:
        chain = [first_word]

    while True:
        curr_word = np.random.choice(word_dict[chain[-1]])
        chain.append(curr_word)
        if any(x in curr_word for x in ('!', '?', '.')) and not any(x in curr_word for x in ('Mr.', 'Ms.', 'Mrs.')):
            return chain


def generate_sentences(first_word, word_dict, text, num_sentences):
    sentences = []
    for i in range(num_sentences):
        if first_word == 'NullNull':
            chain = [np.random.choice(text.split())]
        else:
            chain = [first_word]

        while True:
            curr_word = np.random.choice(word_dict[chain[-1]])
            chain.append(curr_word)
            if any(x in curr_word for x in ('!', '?', '.')) and not any(x in curr_word for x in ('Mr.', 'Ms.', 'Mrs.')):
                sentences.append(chain)
                break
    return sentences


def remove_duplicates(lst):
    dropped_indices = set()
    counter = Counter(tuple(lst[i:i + 2]) for i in range(len(lst) - 1))

    for i in range(len(lst) - 2, -1, -1):
        sub = tuple(lst[i:i + 2])
        if counter[sub] > 1:
            dropped_indices |= {i, i + 1}
            counter[sub] -= 1
    return [x for i, x in enumerate(lst) if i not in dropped_indices]


def cleanup(text):
    text = " ".join(remove_duplicates(text))
    text = text[0:2].capitalize() + text[2:]
    return text


def cleanup_sentences(sentences):
    dirty_sentences = sentences
    clean_sentences = []
    for i in dirty_sentences:
        clean_sentences.append(cleanup(i))
    return clean_sentences


def get_dict(text_file, dict_path):
    json_file_name = 'dict_' + os.path.splitext(text_file)[0] + '.json'
    json_file_path = dict_path + json_file_name
    if not os.path.exists(dict_path):
        os.makedirs(dict_path)
    if path.exists(json_file_path):
        with open(json_file_path) as json_file_path:
            word_dict = json.load(json_file_path)
    else:
        word_dict = make_model(open(text_file).read())
        with open(json_file_path, 'w') as outfile:
            json.dump(word_dict, outfile)
    return word_dict

def get_text_file():
    file_path = input("Source Data File?\n:>\t")
    if path.exists(file_path):
        return file_path
    else:
        print("That is not a valid file. Try again.")
        get_text_file()


def get_num_sentences():
    num = input("How many sentences should be generated?\n:>\t")
    if num.isdigit():
        return num
    else:
        print("That is not an integer. Try again.")
        get_num_sentences()


def get_start_words(text, num_words):
    first_word_raw = input(
        "What is the initial word? Entering nothing will result in a random word for each sentence.\n:>\t")
    first_word = ' ' + first_word_raw + ' '
    word_list = []

    if first_word_raw == '':
        for i in range(num_words):
            word_list.append(np.random.choice(text.split()))

    if first_word.upper() in text.upper():
        print('Using chosen word.')
        for i in range(num_words):
            word_list.append(first_word_raw)
    else:
        if input("Chosen word not found. Chose random words (Y) or select a new word (N) (Y/N)\n:>\t").upper() == 'N':
            get_start_word(text)
        else:
            for i in range(num_words):
                word_list.append(np.random.choice(text.split()))
    return word_list


def get_start_word(text):
    first_word = ' ' + input(
        "What is the initial word? Entering nothing will result in a random word for each sentence.\n:>\t") + ' '

    if first_word == '  ':
        return 'NullNull'
    if first_word.upper() in text.upper():
        print('Using chosen word.')
        first_word = first_word.strip()
    else:
        if input("Chosen word not found. Chose a random word (Y) or select a new word (N) (Y/N)\n:>\t").upper() == 'N':
            get_start_word(text)
        else:
            first_word = np.random.choice(text.split())
    return first_word

def main():
    dict_path = os.getenv('APPDATA') + '\\Markov_Dictionaries\\'
    text_file = get_text_file()
    text = open(text_file).read()
    word_dict = get_dict(text_file, dict_path)
    num_sentences = int(get_num_sentences())
    first_word = get_start_word(text)

    user_option = input(
        "Would you like to: \n1) Save the output to a file\n2) Print output to console\n3) Have the program rapidly output to the cursor.\n:>\t")

    if 1 == int(user_option):
        output_file = open('output_' + text_file, 'a')
        for i in range(num_sentences):
            output_file.write(cleanup(generate_text(first_word, word_dict, text)) + '\n')
        output_file.close()
        input("Done!")

    elif 2 == int(user_option):
        for i in range(num_sentences):
            for j in cleanup_sentences(generate_sentences(first_word, word_dict, text, num_sentences)):
                print(j)
            # print(cleanup(generate_text(first_word, word_dict, text)))
        input("Done!")

    elif 3 == int(user_option):
        print("You have 2 seconds to move the cursor to the desired location.")
        time.sleep(2)
        for i in range(num_sentences):
            output = cleanup(generate_text(first_word, word_dict, text))
            pyautogui.typewrite(output, interval=0.01)
            pyautogui.press('enter')
            time.sleep(0.5)
        input("Done!")

    elif 4 == int(user_option):
        for i in cleanup_sentences(generate_sentences(first_word, word_dict, text, num_sentences)):
            print(i + "\n")

    else:
        print("Invalid option.")

    if input("Would you like to run the program again? (Y/N)\n:>\t").upper() == 'Y':
        main()


if __name__ == "__main__":
    main()
