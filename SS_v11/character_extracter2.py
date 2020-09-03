import MeCab
mecab = MeCab.Tagger('-d  /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
mecab.parse('')
import re
from line_processer import first_processor

def make_pos(line):
    mecab_parsed = mecab.parse(line)
    mecab_parsed = mecab_parsed.split('\n')[:-2]
    token_pos = []
    for tp in mecab_parsed:
        token, pos = tp.split('\t')
        pos1, pos2, _ = pos.split(',', 2)
        token_pos.append((token, [pos1, pos2]))
    return token_pos

def characters_processor(line, characters):
    token_pos = make_pos(line)
    # token_pos = reversed(token_pos)
    bunsetu = []
    for tp in token_pos:
        token, pos = tp
        if '記号' in pos or '助詞' in pos or '助動詞' in pos or '接尾' in pos or '非自立' in pos:
            bunsetu.insert(0, (token, pos))
        else:
            bunsetu.insert(0, (token, pos))
            characters = bunsetu_processor(bunsetu, characters)
    return characters

def bunsetu_processor(bunsetu, characters):
    setubi_flag = False
    hiragana = re.compile('^[\u3041-\u309F]+?$')
    for token, pos in bunsetu:
        if ('接尾' in pos and '名詞' in pos) or ('先生' == token or '先輩' == token or 'センパイ' == token or '。' == token):
            setubi_flag = True
        elif setubi_flag and '固有名詞' in pos:
            if hiragana.search(token) is None:
                characters.add(token)
        elif ('ちゃん' in token or 'チャン' in token or 'さん' in token  or 'サン' in token) and '名詞' in pos:
            characters.add(token)
        else:
            setubi_flag = False
    return characters

def extract_names(texts):
    characters = set()
    res_lines = []
    for text in texts:
        actor = text.split(',')[0]
        line = text.split(',')[1]

        if '・' in actor and '（' not in actor and '(' not in actor:
            actors = actor.split('・')
            for actor in actors:
                characters.add(actor)
        else:
            characters.add(actor)
        line = first_processor(line)
        res_lines.append(actor + ',' + line)
        end = re.compile('[！。、？]$')
        if end.search(line) is None:
            line = line + '。'
        characters = characters_processor(line, characters)
    characters = sorted(characters, key=len, reverse=True)
    return characters, res_lines

if __name__=='__main__':
    import argparse
    import os
    import pprint
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='sshouko')
    parser.add_argument('-f', '--file', required=True)

    args = parser.parse_args()
    dir = args.dir
    file = args.file

    base_path = '/home/maya/PycharmProjects/NarouScraping/SS_v11'
    with open(os.path.join(base_path, dir, file), 'r') as f:
        lines = f.readlines()

    extract_names(lines)


