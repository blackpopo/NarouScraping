from character_extracter2 import extract_names, make_pos
import MeCab
import os
mecab = MeCab.Tagger('-d  /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd ')
mecab.parse('')
import argparse
from line_processer import middle_processor, last_processor
import pprint
import re

def wakati(line):
    parsed = mecab.parse(line).split('\n')[:-2]
    parsed = [p.split('\t')[0] for p in parsed]
    return parsed

def build_line(line, actor, next_actor, characters):
    token_pos = make_pos(line)
    token_pos.reverse()
    bunsetu_list = []
    is_settou = False
    res_line = ''
    for i, (token, pos) in enumerate(token_pos):
        if not is_settou:
            if '記号' in pos or '助詞' in pos or '助動詞' in pos or '接尾' in pos:
                bunsetu_list.append((token, pos))
            elif i+1 < len(token_pos) and '接頭詞' in token_pos[i+1][1]:
                bunsetu_list.append(token_pos[i+1])
            else:
                bunsetu_list.append((token, pos))
                sub_line = bunsetu_processor(bunsetu_list, actor, next_actor, characters)
                res_line = sub_line + res_line
                bunsetu_list = []
        else:
            pass
    return res_line

def bunsetu_processor(bunsetu_list, actor, next_actor, characters):
    res_line = ''
    for token, pos in bunsetu_list:
        if token == next_actor:
            res_line = 'あなた' + res_line
        elif token == actor:
            res_line = '私' + res_line
        elif token in characters:
            return ''
        elif '代名詞' in pos and '君'==token:
            res_line = 'あなた' + res_line
        elif '接尾' in pos and '名詞' in pos and (token == 'さん' or token == 'ちゃん'or token =='チャン'  or token =='サン' or token=='さま' or token=='君' or token=='くん' or token=='クン'):
            pass
        else:
            res_line = token + res_line
    # desunya = re.compile(r'(ですっ|にゃ|ますっ)[。！？]?')
    # if desunya.search(res_line):
    #     res_line = desunya.sub('です。', res_line)
    return res_line

def lines_character_extracter(texts):
    characters, texts = extract_names(texts)
    res_lines = []
    for i, text in enumerate(texts):
        actor = text.split(',')[0]
        line = text.split(',')[1]

        if i+1 == len(texts):
            next_actor = 'No Face'
        else:
            next_actor = texts[i+1].split(',')[0]

        line = middle_processor(line)
        line = build_line(line, actor, next_actor, characters)
        line = last_processor(line)
        res_lines.append(line)
    return res_lines, characters


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, default=None)
    parser.add_argument('-n', '--new', type=bool, default=False)
    args = parser.parse_args()
    dir = args.dir
    file = args.file
    new = args.new
    base_dir = '/home/maya/PycharmProjects/NarouScraping/SS_v11'

    if file is not None:
        files = [file]
    else:
        files = os.listdir(os.path.join(base_dir, dir))

    if new:
        os.remove(os.path.join(base_dir, 'log', dir + '_characters_doubted3.txt'))
        os.remove(os.path.join(base_dir, 'log', dir +'_finished_files3.txt'))

    for i,file in enumerate(files):
        print('{} is starting'.format(file))
        with open(os.path.join(base_dir, dir, file), 'r') as f:
            lines = f.readlines()
        try:
            lines, characters = lines_character_extracter(lines)

            with open(os.path.join(base_dir, dir+'_processed', file), 'w') as f:
                f.write('\n'.join(lines))

            if len(characters) > 5  and len(wakati(characters[4])) > 3:
                with open(os.path.join(base_dir, 'log', dir + '_characters_doubted3.txt'), 'a') as f:
                    f.write('\t'.join([dir, file, *characters])+'\n')

            with open(os.path.join(base_dir, 'log', dir+'_finished_files3'), 'a') as f:
                f.write(file+'\n')
            print('{}% is finished!!!'.format((i+1)/len(files)*100))

        except Exception as err:
            print(err)
            print('-'*96+ ' {} is failed'.format(file))





