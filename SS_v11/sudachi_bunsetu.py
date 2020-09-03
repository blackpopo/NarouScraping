from sudachipy import dictionary
from sudachipy import tokenizer


sudachi = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C

line = 'ゼロ様の言うとおりでいしたわ'
doc = sudachi.tokenize(line, mode)
doc = list(reversed(doc))
bunsetu = ''
bunsetu_list = []
for i, token in enumerate(doc):
    print(token.surface(), token.part_of_speech())
    if '助詞' in token.part_of_speech()[0] or '助動詞' in token.part_of_speech()[0] or '記号' in token.part_of_speech()[0] or ('接尾辞' in token.part_of_speech()[0] and '名詞的' in token.part_of_speech()[1]):
        bunsetu = token.surface() + bunsetu
    else:
        bunsetu = token.surface() + bunsetu
        if i+1<=len(doc)-1 and doc[i+1].part_of_speech()[0] == '接頭辞':
            bunsetu = doc[i+1].surface() + bunsetu
        bunsetu_list.append(bunsetu)
        bunsetu = ''
bunsetu_list.reverse()
print(bunsetu_list)
