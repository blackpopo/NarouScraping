from sudachipy import tokenizer
from sudachipy import dictionary

ginza = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C

import sys
import os

def print_lines(lines):
    for line in lines:
        line = line.rstrip('\n')
        # print(line)
        norm_line = normalize_line(line)
        # print(norm_line)

def normalize_line(line):
    doc = ginza.tokenize(line, mode)
    normalized_line = ''
    for token in doc:
        # print(token.surface(), token.part_of_speech(), token.reading_form(), token.get_word_info(), token.normalized_form(), token.begin(), token.dictionary_form(), token.word_info)
        # normalized_line += token.normalized_form()
        # print(token.surface(), token.part_of_speech())
        if  ('名詞' in token.part_of_speech() or '形容詞' in token.part_of_speech() or '副詞' in token.part_of_speech() or '代名詞' in token.part_of_speech()) and '数詞' not in token.part_of_speech():
            if token.surface() != token.normalized_form():
                print(token.surface(), token.normalized_form(),  token.part_of_speech())
            normalized_line += token.normalized_form()

        else:
            normalized_line += token.surface()
    return normalized_line

if __name__=='__main__':
    base_dir = '/home/maya/PycharmProjects/NarouScraping/SS_v11'
    file_dir, file_name = sys.argv[1: 3]
    file_dir = file_dir + '_processed'
    file_name = file_name + '_processed.txt'
    path = os.path.join(base_dir, file_dir, file_name)
    print(path)
    with open(path, 'r') as f:
        lines = f.readlines()
    print_lines(lines)


# doc_normalized = ginza.tokenize(normalized_line, mode)
# for token in doc_normalized:
#     print(token.surface(), token.normalized_form())