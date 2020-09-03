import MeCab
import os

def TestFileOpen(dir, filename):
    full_path = os.path.join(dir, filename)
    with open(full_path, 'r') as file:
        sentence_list = file.readlines()
    return sentence_list

def subtract_subjects(sentence_list):
    tagger = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    response = []
    for sentence in sentence_list:
        sentence = sentence.replace('…', '').replace('「', '').replace('」', '').replace('\n','').strip()
        if sentence:
            parsed_sentence = tagger.parse(sentence)
            parsed_sentence = parsed_sentence.split('\n')
            response_words = ''
            for word in parsed_sentence:
                if word  not in ['EOS', '']:
                     print(word.split('\t')[1])

if __name__=='__main__':
    dir = '/home/maya/PycharmProjects/NarouScraping/Narou_v10/NarouTopModernRenai'
    file = 'n0690cw.txt'
    sentences = TestFileOpen(dir, file)
    subtract_subjects(sentences)



