# import dialog_extracter
import re
import spacy
spacy.require_gpu()
ginza = spacy.load('ja_ginza')
import mojimoji

bunsetu = '……ちくしょう。提督になればモテモテで殆どの艦は提督に求婚、プロポーズすれば99%成功って聞いていたのに……。いやまてよ、吹雪がその1%の奇跡だった可能性が！。榛名！。'
renzoku = re.compile(r'(.)\1{2,}')
try:
    while renzoku.search(bunsetu):
        start, end = renzoku.search(bunsetu).span()
        bunsetu = bunsetu[:start+1] + bunsetu[end:]
except:
    print('Span Error')
    pass

print(bunsetu.replace('・', ''))

for token in ginza(bunsetu):
    print(token.orth_, token.norm_, token.dep_, token.tag_, token.pos_, token.lemma_)


line = '海馬瀬人のフィールドのブルーアイズを生贄に、青眼の白龍を召喚！！?!’。そしてモンスターすべてでダイレクトアタック！/////。滅びのバーストストリーム！。ﾌﾊﾊﾊﾊ！粉砕！玉砕！大喝采！！！'
ep = re.compile(r'[。、！/]$')

if ep.search(line) is None:
    line = line + '。'

print(line)
line = mojimoji.han_to_zen(line, ascii=False, digit=False)
print(line)
line = mojimoji.zen_to_han(line, kana=False)
print(line)

bunsetu = '知ってる。、'

signs0 = re.compile('…+')
signs1 = re.compile(r'[、？！。]+$')
signs2 = re.compile(r'[、！。]+$')
signs3 = re.compile(r'[、。]+$')
signs4 = re.compile(r'^[、！。]+')
desunya = re.compile(r'(ですっ|にゃ)[。！？]?')

if '…' in bunsetu:
    bunsetu = signs0.sub('、', bunsetu)
if '、' in bunsetu or '！' in bunsetu or '。' in bunsetu:
    bunsetu = signs4.sub('', bunsetu)
if '？' in bunsetu:
    bunsetu = signs1.sub('？', bunsetu)
elif '！' in bunsetu:
    bunsetu = signs2.sub('！', bunsetu)
elif '。' in bunsetu:
    bunsetu = signs3.sub('。', bunsetu)
if desunya.search(bunsetu):
    bunsetu = desunya.sub('です。', bunsetu)

print(bunsetu)