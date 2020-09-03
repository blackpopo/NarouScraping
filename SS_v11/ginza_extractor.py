# import spacy
import sys
import os
import re

# ginza = spacy.load('ja_ginza')

from sudachipy import tokenizer
from sudachipy import dictionary
ginza = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C

file_name = sys.argv[1]

path = os.path.join('./sshouko', file_name)

with open(path, 'r') as f:
    lines = f.readlines()

characters =[]

extract_characters = []

# lines = []

for i, line in enumerate(lines):
    actor, line = line.split(',')
    if actor not in characters:
        if actor != '？':
           characters.append(actor.strip())
    line = line.rstrip('\n')
    line = line.replace('後輩', 'さん').replace('先輩', 'さん')

    xtu = re.compile(u'っ'u'[!！.。]')
    line = xtu.sub('。', line)

    # doc = ginza(line) token.text <->token.surface() token.tag_<->token.part_of_speech
    doc = ginza.tokenize(line, mode)
    zinmei = ''
    temp_zinmei = ''

    nokoto_flag = False
    for token in doc:
        # tag = token.tag_
        # bi = token._.bunsetu_bi_label
        tag = token.part_of_speech()
        if '人名' in tag or '地名' in tag:
            if not token.surface() in extract_characters:
                extract_characters.append(token.surface())
        elif '固有名詞' in tag:
            zinmei = token.surface()
        elif '接尾辞' in tag and '名詞的' in tag and (token.surface() == 'たち' or token.surface() == 'さん'):
            if zinmei != '':
                if not zinmei in extract_characters:
                    extract_characters.append(zinmei)
            elif temp_zinmei != '':
                if not temp_zinmei in extract_characters:
                    extract_characters.append(temp_zinmei)
        elif temp_zinmei != '' and 'こと' == token.surface() and nokoto_flag:
            nokoto_flag = False
            if not temp_zinmei in extract_characters:
                if not temp_zinmei in ['人', '金', '相手', '客']:
                    print(temp_zinmei, line)
                    extract_characters.append(temp_zinmei)
        # elif 'B' == bi and '普通名詞-一般' in tag  or '一般名詞-一般' in tag:
        #     temp_zinmei = token.surface()
        #     nokoto_flag = True
        # elif 'I' == bi and '普通名詞-一般' in tag  or '一般名詞-一般' in tag:
        #     temp_zinmei += token.surface()
        #     nokoto_flag = True
        elif ('普通名詞' in tag  or '一般名詞' in tag) and  '一般'in tag:
            temp_zinmei = token.surface()
        elif temp_zinmei != '' and 'の' == token.surface():
            nokoto_flag = True
        else:
            zinmei = ''
            temp_zinmei = ''
            nokoto_flag = False

characters.extend(extract_characters)

general_characters = ['アイツ', 'センパイ', 'センパーイ', 'パパー', 'ママー']

family_names = ['お兄ちゃん', 'お姉ちゃん','おにーちゃん', 'おねーちゃん', '兄', '姉', '妹', '弟', '母','親父', '父',  'お袋', 'おふくろ', 'パパ', 'ママ']

family_characters = []

for family in family_names:
    family_characters.append(family + 'たち')
    family_characters.append(family + '達')

family_characters.extend(family_names)

characters.extend(general_characters)

characters.extend(family_characters)

# for chara in characters:
#     print(chara)

for i, rline in enumerate(lines):
    actor, line = rline.split(',')
    raw_line = line.rstrip('\n')
    line = raw_line.replace('先輩達', 'さん').replace('先輩たち', 'さん').replace('後輩達', 'さん').replace('後輩たち', 'さん').replace('後輩', 'さん').replace('先輩', 'さん')

    xtu = re.compile(u'っ'u'[!！.。]')
    line = xtu.sub('。', line)

    kana1 = re.compile(u'[.。]'u'[ぁ-ン]'u'、')
    kana2 = re.compile(u'[!！]'u'[ぁ-ン]'u'、')
    kana3 = re.compile(u'[…、]'u'[ぁ-ン]'u'、')
    kasira = re.compile('^'u'[ぁ-ン]'u'[、。！]')
    line = kana1.sub('。', line)
    line = kana2.sub('！', line)
    line = kana3.sub('', line)
    line = kasira.sub('', line)

    for syn in [actor, '俺', 'オレ', '僕', 'ボク', 'ウチ', 'おれ', 'わたし', 'ワタシ']:
        line = line.replace(syn, '私')

    if i + 1 >= len(lines):
        break

    next_actor = lines[i + 1].split(',')[0]

    if next_actor in line:
        line = line.replace(next_actor, 'あなた')
    for syn in ['あなた達','貴方達', '貴方', 'アナタ', '貴様', 'テメ', 'テメー', 'お前ら','てめぇ', 'お前', 'おまえ']:
        line = line.replace(syn, 'あなた')


    for character in characters:
        if character in line:
            line = line.replace(character, '山田')

    for before, after in zip(['くんっ', 'まつ', 'ちゃーん'], ['さん', '待つ', 'さん']):
        line = line.replace(before, after)


    # doc = ginza(line) token.text <->token.surface() token.tag_<->token.part_of_speech
    doc = ginza.tokenize(line, mode)
    new_line = ''

    zinmei_flag = False
    setsubizi_flag = False
    zyoshi_flag = False
    kigou_flag = False
    daimeishi_flag = False
    meyou_flag = False

    for token in doc:
        # tag = token.tag_
        tag = token.part_of_speech()
        if '人名' in tag:
            zinmei_flag = True
        elif ('接尾辞' in tag and '名詞的' in tag) and (zinmei_flag or daimeishi_flag):
            zinmei_flag = False
            daimeishi_flag = False
            setsubizi_flag = True
        elif '助詞' in tag and (zinmei_flag or daimeishi_flag):
            zinmei_flag = False
            daimeishi_flag = False
            zyoshi_flag = True
        elif '補助記号' in tag and (zinmei_flag or daimeishi_flag):
            zinmei_flag = False
            daimeishi_flag = False
            kigou_flag = True
        elif '助詞' in tag and setsubizi_flag:
            setsubizi_flag = False
            zyoshi_flag = True
            if meyou_flag:
                new_line += token.surface()
                zyoshi_flag = False
        elif 'こと' == token.surface() and zyoshi_flag:
            pass
        elif '助詞' in tag and zyoshi_flag:
            pass
        elif '補助記号' in tag and setsubizi_flag:
            setsubizi_flag = False
            kigou_flag = True
        elif '補助記号' in tag and zyoshi_flag:
            zyoshi_flag = False
            kigou_flag = True
        elif '代名詞' in tag and (token.surface() == '彼女' or token.surface() == '彼'):
            daimeishi_flag = True
        elif '代名詞' in tag and (token.surface() == 'あなた' or token.surface() == '私'):
            meyou_flag = True
            new_line += token.surface()
        elif '代名詞' in tag and token.surface() == '君':
            new_line += 'あなた'
            daimeishi_flag = True
        elif '代名詞' in tag and zinmei_flag:
            zinmei_flag = False
            new_line += token.surface()
        elif zinmei_flag:
            zinmei_flag = False
            new_line += token.surface()
        elif '山田' == token.surface():
            zinmei_flag = True
        elif ('さん' == token.surface() or 'くん' == token.surface()) and ('接尾辞' in tag and '名詞的' in tag):
            setsubizi_flag = True
        elif '接尾辞' in tag and '名詞的' in tag and daimeishi_flag:
            daimeishi_flag = False
            if not meyou_flag:
                setsubizi_flag = True
        else:
            if zinmei_flag or setsubizi_flag or zyoshi_flag or daimeishi_flag or kigou_flag:
                zinmei_flag = False
                setsubizi_flag = False
                zyoshi_flag = False
                kigou_flag = False
                daimeishi_flag = False
                meyou_flag = False
            new_line += token.surface()

    if new_line == '':
        new_line = 'No comment!'


    if raw_line != new_line:
        print(rline)
        print(new_line)
