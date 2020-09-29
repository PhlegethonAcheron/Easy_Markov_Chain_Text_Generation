# import json
# import mimetypes
# import os
# from collections import Counter
# from os import path
#
# import numpy as np
#
# def make_pairs(text):
#     text = text.split()
#     for i in range(len(text)-1):
#         yield text[i], text[i + 1]
#
# def make_dict(pairs):
#     word_dict = {}
#     for word_1, word_2 in pairs:
#         if word_1 in word_dict.keys():
#             word_dict[word_1].append(word_2)
#         else:
#             word_dict[word_1] = [word_2]
#     return word_dict
#
# def train_model(text):
#     pairs = make_pairs(text)
#     word_dict = make_dict(pairs)
#     return word_dict
#
# def generate_text(first_word, text, word_dict):
#     if first_word in text:
#         print('Using chosen word.')
#         first_word = first_word.strip()
#     else:
#         print('Chosen word not found. Using random word.')
#         first_word = np.random.choice(text.split())
#     chain = [first_word]
#
#     while True:
#         curr_word = np.random.choice(word_dict[chain[-1]])
#         chain.append(curr_word)
#         if any(x in curr_word for x in ('!', '?', '.')) and not any(x in curr_word for x in ('Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Sr.')):
#             return chain
#
# def remove_duplicates(lst):
#     dropped_indices = set()
#     counter = Counter(tuple(lst[i:i+2]) for i in range(len(lst) - 1))
#
#     for i in range(len(lst) - 2, -1, -1):
#         sub = tuple(lst[i:i+2])
#         if counter[sub] > 1:
#             dropped_indices |= {i, i + 1}
#             counter[sub] -= 1
#     return [x for i, x in enumerate(lst) if i not in dropped_indices]
#
# def cleanup(text):
#     text = " ".join(remove_duplicates(text))
#     # text = text.strip('[]')
#     # text = text.replace("',", "")
#     # text = text.replace("'", "")
#     text = text[0:2].capitalize() + text[2:]
#     return text
#
# def get_dict(text_file):
#     json_file_name = 'dict_' + os.path.splitext(text_file)[0] + '.json'
#     if path.exists(json_file_name):
#         with open('dict_' + os.path.splitext(text_file)[0] + '.json') as json_file:
#             word_dict = json.load(json_file)
#     else:
#         word_dict = train_model(open(text_file).read())
#         with open('dict_' + os.path.splitext(text_file)[0] + '.json', 'w') as outfile:
#             json.dump(word_dict, outfile)
#         # print("json file created successfully")
#     return word_dict
#
# def get_text_file():
#     file_path = input("Source Data File?\n:>\t")
#     if path.exists(file_path):
#         return file_path
#     else:
#         print("That is not a valid file. Try again.")
#         get_text_file()
#
# def get_num_sentences():
#     num = input("How many sentences should be generated?\n:>\t")
#     if num.isdigit():
#         return num
#     else:
#         print("That is not an integer. Try again.")
#         get_num_sentences()
#
# def get_start_word():
#     start_string = ' ' + input("What is the starting word?\n:>\t") + ' '
#     return start_string
#
# def main_bit_manual():
#     text_file = get_text_file()
#     text = open(text_file).read()
#     word_dict = get_dict(text_file)
#     num_sentences = int(get_num_sentences())
#     start_string = get_start_word()
#     for i in range(num_sentences):
#         output = cleanup(generate_text(start_string, text, word_dict))
#         print(output)
#
# main_bit_manual()
