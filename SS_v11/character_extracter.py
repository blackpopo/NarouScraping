#character をBIを用いて、抜き出す！
import spacy
import mojimoji
import sys
import os
import re
from sudachipy import dictionary
from sudachipy import tokenizer
from line_processer import first_processor

def extract_names(lines, sudachi, mode):
    characters = set()
    return_lines = []
    for line in lines:
        actor = line.split(',')[0]
        line = line.split(',')[1]

        signs = re.compile(r'[（）【】、！。？]')
        if not signs.search(actor):
            if '・' in actor:
                actors = actor.split('・')
                for actor in actors:
                    characters.add(actor)
            else:
                characters.add(actor)

        line = first_processor(line)

        return_lines.append(actor+','+line)

        try:
            doc = sudachi.tokenize(line, mode)
            doc = list(reversed(doc))
        except:
            doc = ''
        bunsetu = []
        settou_flag = False
        for id, token in enumerate(doc):
            if not settou_flag:
                tag = token.part_of_speech()
                bi = tag[0]
                text = token.surface()
                norm = token.normalized_form()

                if '記号' in bi or '助詞' in bi or '助動詞' in bi:
                    bunsetu.insert(0, (text, tag))
                elif ('接尾辞' in tag[0] and '名詞的' in tag[1]):
                    bunsetu.insert(0, (norm, tag))
                else:
                    bunsetu.insert(0, (text, tag))
                    if id + 1 <= len(doc) - 1:
                        if doc[id + 1].part_of_speech()[0] == '接頭辞':
                            bunsetu.insert(0, (doc[id+1].surface(), doc[id+1].part_of_speech()))
                            settou_flag = True
                    characters = extract_chara(bunsetu, characters)
                    bunsetu = []
            elif settou_flag:
                settou_flag = False

    characters = sorted(characters, key=len, reverse=True)
    hiragana = re.compile('^[\u3041-\u309F][\u309b\u309c]?$')
    katakata = re.compile('^[\u30a1-\u30fa\u30fc][\u309b\u309c]?$')
    characters = [chara for chara in characters if hiragana.search(chara) is None and katakata.search(chara) is None]

    return list(characters), return_lines

def extract_chara(bunsetu_list, characters):
    chara_candi = ''

    san = re.compile('(.*?)(' u'さん' '|' u'ちゃん' '|' u'くん' '|' u'サン' '|' u'チャン' '|' u'クン'')$')

    for text, tag in bunsetu_list:
        if '普通名詞' in tag and san.match(text) is not None:
            characters.add(text)
            if san.search(text).group(1) != '':
                characters.add(san.search(text).group(1))
        elif '人名' in tag or '地名' in tag:
            characters.add(text)
            chara_candi += text
        elif 'センパイ' == text or '先輩' == text:
            if chara_candi != '':
                characters.add(chara_candi)
        elif ('普通名詞' in tag and '一般' in tag) or '固有名詞' in tag or '接頭辞' in tag:
            chara_candi += text
        elif ('さん' == text or 'くん' == text or 'ちゃん' == text or 'たち' == text or '達' == text or '君' == text or 'さま'==text or '様'==text or '殿'==text) and '接尾辞' in tag:
            if chara_candi != '':
                characters.add(chara_candi)
        elif '！' == text or '？' == text or '。' == text:
            # if chara_candi != '' and hiragana.match(chara_candi) is None and katakata.match(chara_candi) is None and len(bunsetu_list) >= 2 and len(chara_candi) > 1:
            #     characters.add(chara_candi)
            if chara_candi != '' and len(bunsetu_list) == 2 and len(chara_candi) > 3:
                characters.add(chara_candi)
        elif '動詞' in tag or '形容詞' in tag:
            break
        else:
            chara_candi = ''
    return characters

if __name__=='__main__':
    sudachi = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C

    file_dir, file_name = sys.argv[1: 3]

    file_path = os.path.join('./'+file_dir, file_name)

    with open(file_path, 'r') as f:
        lines = f.readlines()

    characters, return_lines = extract_names(lines, sudachi, mode)

    characters = sorted(characters, key=len, reverse=True)

    print(characters)
    print(len(return_lines))
