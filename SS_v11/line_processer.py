import re
import mojimoji

#()の中身は…消去！
def first_processor(line):
    line = line.rstrip('\n')

    line = mojimoji.han_to_zen(line, ascii=False, digit=False)
    line = mojimoji.zen_to_han(line, kana=False)

    # 特殊事例の語尾、記号を排除
    # 名前を取り出すための処理
    setubi_dis = ['さぁん', 'ますっ', 'ちゃーん', 'ちゃぁん', 'くーん', 'さーん', 'くんっ', 'さんっ']
    setubi_ori = ['さん', 'ます', 'ちゃん', 'ちゃん', 'くん', 'さん', 'くん', 'さん']
    replace_dis = ['～', '-', '❤', '♡', '.', ',', '!', '/', '?', '・', "’", '~', '―', '(', ')', '…']
    replace_ori = ['ー', 'ー', '。', '。',  '、', '、', '！', '！', '？', '、',  "'", 'ー', 'ー', '（', '）', '、']
    space_dis = ['♪', '■', '↓',  'ww', '★', '☆', 'ｗｗ', '♥', '＞', '"', '♂', '♀', '→', '>', '○', '〇', '”', '“', ' ', '　', '〝', '〟', '《', '》', '【', '】']
    space_ori = [''] * len(space_dis)
    destinations = setubi_dis + replace_dis + space_dis
    originals = setubi_ori + replace_ori + space_ori
    for dst, ori in zip(destinations, originals):
        line = line.replace(dst, ori)

    xtu = re.compile(u'っ'u'[！。]')
    line = xtu.sub('。', line)
    kakko = re.compile(r'[（].*?[）]')
    line = kakko.sub('', line)
    dots = re.compile(r'、{2,}')
    line = dots.sub('、', line)
    renzoku1 = re.compile(r'(.)\1{2,}')
    while renzoku1.search(line):
        start, end = renzoku1.search(line).span()
        line = line[:start] + line[end:]

    # 伸ばし棒を何個もつけんな
    bars = re.compile(r'ー+')
    line = bars.sub(r'ー', line)
    # # 日本語ー記号のーを消去
    jbar = re.compile(r'(.+?)([\u3041-\u309F]|[\u309b\u309c]|[々〇〻\u3400-\u9FFF\uF900-\uFAFF]|[\uD840-\uD87F]|[\uDC00-\uDFFF])(ー)([？！、。]|$)')
    def middel_skip(m_list):
        m_list = [m for m in m_list if  m != '' and m !='ー']
        return ''.join(m_list)
    if jbar.search(line):
        line = middel_skip(jbar.split(line))
    line = line.lstrip('、')
    return line

def middle_processor(line, you=None):
    myself = ['俺', 'オレ', '僕', 'ボク', 'ウチ', 'おれ', 'わたし', 'ワタシ', 'アタシ', 'あたし', 'わしゃ', 'ワシ', '儂', 'わたくし', 'ワタクシ', 'オイラ', 'おいら']
    yourself = ['あなた達', '貴方達', '貴方', 'アナタ', '貴様', 'テメ', 'テメー', 'お前ら', 'てめぇ', 'お前', 'おまえ', 'キミ', 'きみ', 'あなたっ', 'アンタ', 'てめェ', 'あんた']
    if you is not None:
        yourself.extend(you)
    # 登場人物に「俺くん」と言うやつがいて、そいつのために２人称から入れ替え
    for syn in myself:
        line = line.replace(syn, '私')

    for syn in yourself:
        line = line.replace(syn, 'あなた')
    return line

def last_processor(line):
    # 「一文字、」のやつを排除
    kana1 = re.compile(u'[。]'u'[ぁ-ン]'u'[、！。]')
    kana2 = re.compile(u'[！]'u'[ぁ-ン]'u'[、！。]')
    kana3 = re.compile(u'[、]'u'[ぁ-ン]'u'[、！。]')
    kana4 = re.compile(u'[？]'u'[ぁ-ン]'u'[、！。]')
    kasira1 = re.compile('^'u'[ぁ-ン]'u'[ぁァぇェぅゥぃィぉォッっ]?'u'[、。！]')
    kasira2 = re.compile('^'u'[ぁ-ン]'u'[ぁァぇェぅゥぃィぉォッっ]?$')
    kasira3 = re.compile('^[0-9]+$')
    # dots = re.compile(r'、{2,}')
    #
    #
    # while dots.search(line):
    #     start, end = dots.search(line).span()
    #     line = line[:start] + line[end:]

    line = line.rstrip('、')
    line = kana1.sub('。', line)
    line = kana2.sub('！', line)
    line = kana3.sub('、', line)
    line = kana4.sub('？', line)
    line = kasira1.sub('', line)
    line = kasira2.sub('', line)
    line = kasira3.sub('', line)

    signs1 = re.compile(r'[、？！。]{2,}')
    signs2 = re.compile(r'[、！。]{2,}')
    signs3 = re.compile(r'[、。]{2,}')
    signs4 = re.compile(r'[、]{2,}')

    if '？' in line:
        line = signs1.sub('？', line)
    elif '！' in line:
        line = signs2.sub('！', line)
    elif '。' in line:
        line = signs3.sub('。', line)
    elif '、' in line:
        line = signs4.sub('、', line)

    # 空白分はノーコメントで！
    if line.strip() == '':
        line = 'No Comment'

    # 行頭の！？を消去
    gyoutou = re.compile(r'^[！？。、].+')
    if gyoutou.match(line):
        line = line[1:]

    line = line.rstrip('、')
    gyoumatu = re.compile(r'[！？。]$')
    if not gyoumatu.search(line):
        line += '。'
    return line

def total_processor(line):
    line = first_processor(line)
    line = middle_processor(line)
    line = last_processor(line)
    return line
    
if __name__=='__main__':
    text = '５！？え！？５粒も使ったら私どうされるの！？'
    text = first_processor(text)
    print(text)
    text = middle_processor(text)
    print(text)
    text = last_processor(text)
    print(text)