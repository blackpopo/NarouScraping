import mojimoji
import sys
import os
if __name__=='__main__':
    print('digit, ascii: zen_to_han')
    print('kana: han_to_zen')
    print('input file_dir file_name')
    file_dir, file_name = sys.argv[1: 3]

    base_dir = '/home/maya/PycharmProjects/NarouScraping/SS_v11'

    with open(os.path.join(base_dir, file_dir, file_name)) as f:
        lines = f.readlines()

    lines = [line.rstrip('\n') for line in lines]
    new_lines = []

    for line in lines:

        line = mojimoji.han_to_zen(line, ascii=False, digit=False)
        line = mojimoji.zen_to_han(line, kana=False)

        new_lines.append(line)
    for old, new in zip(lines, new_lines):
        print(old)
        print(new)
        # print('\n')