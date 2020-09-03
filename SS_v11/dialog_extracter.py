import character_extracter
import sys
import os
import re
import mojimoji
from line_processer import middle_processor, last_processor

from sudachipy import tokenizer
from sudachipy import dictionary

# spacy.require_gpu()
# ginza = spacy.load('ja_ginza')

sudachi = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C

def make_dialog(lines):

    characters, lines = character_extracter.extract_names(lines, sudachi, mode)

    characters.extend(['パパ', 'ママ', 'おじ', 'おば', 'いとこ','彼女', '彼', '兄', '姉', '妹', '弟'])

    sentenses = []

    for i, line in enumerate(lines):
        #line の構造は actor,line
        actor = line.split(',')[0]
        line = line.split(',')[1]

        if i+1 >= len(lines):
            next_actor = 'John Smith'
        else:
            next_actor = lines[i+1].split(',')[0]

        line = middle_processor(line)
        bunsetu_list = []
        new_line = ''
        try:
            doc = sudachi.tokenize(line, mode)
            doc = list(reversed(doc))
        except:
            doc = ''
        #後ろの単語から処理している。そうじゃないと、文節取り出すの面倒くさい
        settou_flag = False
        for id, token in enumerate(doc):
            if not settou_flag:
                tag = token.part_of_speech()
                bi = tag[0]
                text = token.surface()
                norm = token.normalized_form()
                norm_dir = {'余り': (['あまり', 'あんまり', 'あんま', 'あんまし', '余り'], 'あまり'),
                             '話': (['話し', '話', 'はなし'], '話'),
                             '強い': (['つええ', 'つえぇ', '強え'], '強え'),
                             '宜しく': (['ヨロシク', 'よろしく', 'よろしゅう', '宜しく'], 'よろしく'),
                             'くす': (['クスッ', 'くすっ'], 'クスッ'),
                             'すっ': (['スッ', 'すっ'], 'スッ'),
                             'びく': (['ビクッ', 'びくっ'], 'ビクッ'),
                             'ちっ': (['チッ', 'ちっ'], 'チッ'),
                             'くっ': (['クッ', 'くっ', ], 'クッ'),
                             'きり': (['キリッ', 'キリッ'], 'キリッ'),
                             'びし': (['ビシッ', 'びしっ'], 'ビシッ'),
                             'ばし': (['バシッ', 'ばしっ'], 'バシッ'),
                             'がら': (['ガラッ', 'がらっ' ], 'ガラッ'),
                             'ぱん': (['パンッ', 'ぱんっ'], 'パンッ'),
                             'ひい': (['ヒイッ', 'ひいっ'], 'ヒイッ'),
                             '煩い': (['うるさ', '五月蝿い', 'うるせえ', 'うっさい', 'うるせぇ', 'ウルサイ', 'うるせー', 'ウルサい'], 'うるさい'),
                             '考': (['考え', '考', 'かんがえ'], '考え'),
                             '白': (['しら', 'シラ'], 'しら'),
                             'ちょろい': (['ちょろっ', 'ちょろい', 'ちょろ', 'チョロい'], 'ちょろい'),
                             '切る': (['切り', '斬り'], '切り'),
                             '匂う': (['くせえ', 'くさ', 'くさっ', 'くさい', 'くせえ', '臭'], 'くさい'),
                             '違う': (['ちがう', '違う', 'ちゃう'], '違う'),
                             'そう': (['そっ', 'そー', 'そう'], 'そう'),
                             '通り': (['とおり', 'とーり', 'どおり', 'どうり'], '通り'),
                             }

                if norm in norm_dir.keys():
                    if text in norm_dir[norm][0]:
                        text = norm_dir[norm][1]

                if '記号' in bi or '助詞' in bi or '助動詞' in bi or ('接尾辞' in tag[0] and '名詞的' in tag[1]):
                    bunsetu_list.insert(0, (text, tag))
                    if id==len(doc)-1:
                        new_line = text + new_line
                else:
                    bunsetu_list.insert(0, (text, tag))
                    if id + 1 <= len(doc) - 1:
                        if doc[id+1].part_of_speech()[0] == '接頭辞':
                            bunsetu_list.insert(0, (doc[id+1].surface(), doc[id+1].part_of_speech()))
                            settou_flag = True
                    bunsetu = chara_check(bunsetu_list, characters, actor, next_actor)
                    new_line = bunsetu + new_line
                    bunsetu_list = []
            else:
                settou_flag = False

        new_line = last_processor(new_line)
        sentenses.append(new_line)

    return sentenses, characters


def chara_check(bunsetu_list, characters, actor, next_actor):
    #一人称、二人称は私、あなたに変えたことによる弊害 あなたさんとか
    #三人称はcharacters のことばが含まれている時点で''を返す。

    bunsetu = ''

    for text, tag in bunsetu_list:
        if text==actor:
            bunsetu+='私'
        elif text==next_actor:
            bunsetu+='あなた'
        elif (text == '私' or text == 'あなた') and '代名詞' in tag:
            bunsetu += text
        elif text in characters or bunsetu in characters:
            return ''
        elif text == 'ワイ' and '代名詞' in tag:
            bunsetu += '私'
        elif text == '君' and '代名詞' in tag:
            bunsetu += 'あなた'
        elif '接尾辞' in tag[0] and '名詞的' in tag[1] and (text == 'さん' or text == 'ちゃん' or text == 'くん' or text =='チャン' or text =='クン' or text =='サン' or text=='さま' or text=='殿' or text=='っぺ'):
            pass
        else:
            bunsetu += text

    desunya = re.compile(r'(ですっ|にゃ)[。！？]?')

    if desunya.search(bunsetu):
        bunsetu = desunya.sub('です。', bunsetu)

    return bunsetu

if __name__=='__main__':

    file_dir = sys.argv[1]
    file_dir = './' + file_dir
    if os.path.isdir(file_dir):
        file_names = os.listdir(file_dir)
    else:
        file_dir, file_names =  file_dir.rsplit('/', 1)
        file_names = [file_names]

    character_doubted_log = os.path.join('./log', file_dir + 'characters_doubted2.txt')
    finished_file_log = os.path.join('./log', file_dir+'_finished_files2.txt')
    if os.path.isfile(character_doubted_log):
        os.remove(character_doubted_log)
    if os.path.isfile(finished_file_log):
        os.remove(finished_file_log)

    for file_name in  file_names:
        print(file_name, 'is started')

        with open(os.path.join(file_dir, file_name), 'r') as f:
            lines = f.readlines()

        save_file_dir = file_dir + '_processed'
        try:
            lines, characters = make_dialog(lines)

            if len(list(sudachi.tokenize(characters[0], mode))) > 3 and len(list(sudachi.tokenize(characters[1], mode))) > 3:
                with open(character_doubted_log, 'a') as f:
                    f.write(file_name + '\n' + '\t'.join(characters) + '\n')

        except  Exception as err:
            print(str(type(err)))
            print(err.args)
            print(str(err))
            with open(os.path.join('./log', 'error.txt'), 'a') as f:
                f.write(file_dir + '\t' + file_name + '\n')
        print(file_name, 'is finished')
        with open(os.path.join(save_file_dir, file_name), 'w') as f:
            f.write('\n'.join(lines))

        with open(finished_file_log, 'a') as f:
            f.write(file_name + '\n')


