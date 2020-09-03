import sys
import os
from collections import Counter
from collections import defaultdict
from sudachipy import tokenizer
from sudachipy import dictionary
ginza = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.A
import json

def sudachi_counter(lines, counter, normalized_counter, original2norm, norm2original):
    for line in lines:
        line = line.rstrip('\n')
        try:
            doc = ginza.tokenize(line, mode)
        except:
            doc = 'UNK'

        count_list = []
        normalized_count_list = []
        for token in list(doc):
            if ('名詞' in token.part_of_speech() or '形容詞' in token.part_of_speech() or '副詞' in token.part_of_speech() or '代名詞' in token.part_of_speech() or '動詞' in token.part_of_speech() or '形容動詞' in token.part_of_speech()) and '数詞' not in token.part_of_speech():
                if token.surface() != token.normalized_form():
                    normalized_count_list.append(token.normalized_form())
                    count_list.append(token.surface())
                    original = token.surface()
                    norm = token.normalized_form()
                    if not original in original2norm:
                        original2norm[original] = [norm]
                    else:
                        if norm not in original2norm[original]:
                            original2norm[original].append(norm)
                    if not norm in norm2original:
                        norm2original[norm] = [original]
                    else:
                        if original not in norm2original[norm]:
                            original2norm[norm].append(original)
                        
        counter.update(count_list)
        normalized_counter.update(normalized_count_list)


if __name__=='__main__':
    dir = sys.argv[1]
    base_dir = '/home/maya/PycharmProjects/NarouScraping/SS_v11'
    dir_path = os.path.join(base_dir, dir)
    file_names = os.listdir(dir_path)
    cnt = 0

    normalized_counter = Counter()
    counter = Counter()
    original2norm = defaultdict(list)
    norm2original = defaultdict(list)

    for file_name in file_names:
        full_path = os.path.join(base_dir, dir_path, file_name)
        with open(full_path, 'r') as f:
            lines = f.readlines()
        print(file_name, 'is started')
        cnt += 1
        sudachi_counter(lines, counter, normalized_counter, original2norm, norm2original)
        if (cnt+1) % 10 == 0:
            with open(os.path.join(base_dir, 'log', 'counter2.txt'), 'w') as f:
                keys = counter.keys()
                for key in keys:
                    diff =  normalized_counter[key] - counter[key]
                    if diff >= 3:
                        original_list = []
                        for norm_key in original2norm[key]:
                            original_list.extend(norm2original[norm_key])
                        f.write(key + '\t' + str(diff) + '\tOriginal2Norm\t' + ' '.join(original2norm[key]) + '\tNorm2Original\t'  + ' '.join(original_list) +  '\n')
