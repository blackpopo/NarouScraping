import os
import spacy
import re

ginza = spacy.load('ja_ginza')

log_dir = './log'

possibly_paths = []

with open(os.path.join(log_dir, 'error.txt'), 'r') as f:
    file_names = f.readlines()

file_names = [f_name.rstrip('\n') for f_name in file_names ]

dirs = ['esusokuhou', 'yomikomu', 'sshouko']

for file in file_names:
    for dir in dirs:
        path = os.path.join(dir, file)
        if os.path.isfile(os.path.join(dir, file)):
            possibly_paths.append(path)

for path in possibly_paths:
    with open(path, 'r') as f:
       lines = f.readlines()
       for line in lines:
           try:
               actor = line.split(',')[0]
               line = line.split(',')[1]
               ep = re.compile(r'[。、！/]$')
               signs = re.compile(r'['u'（'u'）'u'？'u'！'u'、'']')
               if ep.search(line):
                   line = line + '。'

               xtu = re.compile(u'っ'u'[!！.。]')
               line = xtu.sub('。', line)
               kakko = re.compile(r'[(（].*?[）)]')
               line = kakko.sub('', line)
               renzoku1 = re.compile(r'(.)\1{2,}')
               renzoku2 = re.compile(r'(.゛)\1{2,}')
               while renzoku1.search(line):
                   start, end = renzoku1.search(line).span()
                   line = line[:start] + line[end:]
               while renzoku2.search(line):
                   start, end = renzoku2.search(line).span()
                   line = line[:start] + line[end:]
               line = line.replace('ちゃーん', 'ちゃん').replace('くーん', 'くん').replace('さーん', 'さん')
           except:
               print(path)
           try:
               doc = ginza(line)
           except:
               print('ERROR LINE: ', line)
               with open(os.path.join(log_dir, 'error_detail.txt'), 'a') as f:
                   f.write(path + '\t' + line)
