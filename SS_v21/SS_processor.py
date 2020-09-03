import re
# ここで会話文の抜き出し
"""
process_text >> clean_data , line_adder >> get_actor_line
"""
def process_text(texts):
    lines = list()
    for text in texts:
        line = text.replace('\n', '').replace('\u3000', '').replace(' ', '').strip()
        if line != "":
            lines.append(line)
    texts = line_adder(lines)
    descriptive_count = 0
    line_count = 0
    res_lines = list()
    patterns = re.compile('(.*?)[（「｢『](.*)[）｣」』]')
    # print(texts)
    for text in texts:
        if patterns.search(text) != None:
            pat = patterns.search(text).groups()
            actor = pat[0].strip()
            line = pat[1].strip()
            if actor != '':
                line_count += 1
                res_lines.append((actor, line))
            else:
                descriptive_count += 1
        else:
            descriptive_count += 1
    # print(res_lines)
    if descriptive_count < line_count and len(res_lines) != 0:
        print('Success', line_count, descriptive_count)
        return clean_data(res_lines)
    else:
        print('Failure!', line_count, descriptive_count)
        return None

def clean_data(res_lines):
    al_data = get_actor_line(res_lines)
    cor_actor, cor_line = al_data[0]
    res_lines = list()
    for actor, line in al_data[1:]:
        if cor_actor == actor:
            cor_line = cor_line + '。' + line
        else:
            res_lines.append(cor_actor + ',' + cor_line)
            cor_actor = actor
            cor_line = line
    res_lines.append(cor_actor + ',' + cor_line)
    return res_lines


def get_actor_line(texts):
    texts = [(actor, line.strip().replace('『', '').replace('』', '').replace('【', '').replace(
        '】', '')) for actor, line in texts]
    return texts

def line_adder(lines):
    res_lines = list()
    temp_line = ''
    line_flag = False
        
    for line in lines:
        if '「' in line and line_flag:
            if '」' in line:
                line_flag = False
                res_lines.append(line)
                res_lines.append(temp_line)
                temp_line = ''
            else:
                res_lines.append(temp_line + '」')
                temp_line = line
        elif '「' in line and '」' not in line:
            temp_line += line
            line_flag = True
        elif line_flag:
            temp_line += line
            if '」' in line:
                line_flag = False
                res_lines.append(temp_line)
                temp_line = ''
        else:
            res_lines.append(line)
    return res_lines
    
    
if __name__=='__main__':
    url = 'http://blog.livedoor.jp/kokon55/archives/1068474857.html?ref=popular_article&id=6056135-2941642'
    import requests
    from bs4 import BeautifulSoup

    def get_article(link):
        lines = list()
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'lxml')
        # for i in soup.select("br"):
        #     i.replace_with("\n")
        texts = soup.select_one('div.article-body-inner')
        texts = texts.select('div.main_txt')
        for text in texts:
            lines.extend(text.get_text('.').split('.'))
        texts = process_text(lines)
        with open('test_1068474857', 'w') as f:
            f.write('\n'.join(texts))
    get_article(url)