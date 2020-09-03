import spacy

ginza = spacy.load('ja_ginza')

with open('./sshouko/5088.txt', 'r') as f:
    lines = f.readlines()

charaters = lines[0].split(' ')

print(charaters)

for line in lines[1:]:
    line = line.split(',')
    actor = line[0]
    line = line[1].rstrip('\n')

    for chara in charaters:
        line = line.replace('先輩', 'さん').replace('後輩', 'さん')

    doc = ginza(line)
    new_line = ''

    propn_flag = False
    pron_flag = False
    setubizi_flag = False
    zyosi_flag = False

    for i, token in enumerate(doc):
        zinmei = ''
        tag = token.tag_
        if '名詞' in tag:
            propn_flag = True
        elif '接尾辞' in tag and propn_flag:
            setubizi_flag = True
            propn_flag = False
        elif '助詞' in tag and setubizi_flag:
            setubizi_flag = False
            zyosi_flag = True
        elif '記号'in tag and setubizi_flag:
            setubizi_flag = False
            zyosi_flag = True
        elif '助詞' in tag and zyosi_flag:
            zyosi_flag = False
        elif '記号' in tag and zyosi_flag:
            zyosi_flag = False
        else:
            if setubizi_flag or zyosi_flag:
                setubizi_flag = False
                zyosi_flag = False
            new_line += token.text
    print(line)
    print(new_line)

