import os
from pathlib import Path

import numpy as np


class MarkovText:
    def __init__(self, text_path, first_word=False, raw_output=False, remake_dict=False, sentence_mode=True):
        self.text_path = text_path
        self.raw_output = raw_output
        self.remake_dict = remake_dict
        self.dict_path = Path(os.getenv('APPDATA') + '\\Markov_TextGen\\Dicts\\')
        self.dict_list = self.get_existing_dicts()
        self.sentence_mode = sentence_mode
        self.first_word = first_word
        # self.start_words = get_start_words

    def get_existing_dicts(self):
        dict_list = []
        if self.dict_path.exists():

            for i in os.listdir(self.dict_path):
                if self.dict_path.suffix == '.json' and 'dict_' in self.dict_path.stem:
                    dict_list.append(Path(i))
            return dict_list
        else:
            os.makedirs(self.dict_path)
            return dict_list

    def make_pairs(self):
        text = open(self.text_path).read().split()
        for i in range(len(text) - 1):
            yield text[i], text[i + 1]

    def make_dict(self):
        word_dict = {}
        for word_1, word_2 in self.make_pairs():
            if word_1 in word_dict.keys():
                word_dict[word_1].append(word_2)
            else:
                word_dict[word_1] = [word_2]
        return word_dict

    # def get_dict(self):

    def generate_text(self, word_dict):
        if not self.first_word:
            chain = [np.random.choice(open(self.text_path).read.split())]
        else:
            chain = [self.first_word]

        while True:
            curr_word = np.random.choice(word_dict[chain[-1]])
            chain.append(curr_word)
            if any(x in curr_word for x in ('!', '?', '.')) and not any(x in curr_word for x in ('Mr.', 'Ms.', 'Mrs.')):
                return chain

    def generate_sentences(self, word_dict, num_sentences):
        sentences = []
        for i in range(num_sentences):
            if self.first_word == 'NullNull':
                chain = [np.random.choice(open(self.text_path).read.split())]
            else:
                chain = [self.first_word]

            while True:
                curr_word = np.random.choice(word_dict[chain[-1]])
                chain.append(curr_word)
                if any(x in curr_word for x in ('!', '?', '.')) and not any(
                        x in curr_word for x in ('Mr.', 'Ms.', 'Mrs.')):
                    sentences.append(chain)
                    break
        return sentences
