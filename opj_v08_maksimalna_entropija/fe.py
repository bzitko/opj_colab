# coding=utf-8
import re

FILENAME = 'alan_ford_001_grupa_tnt.txt'

def read_file(filename):
    return open(filename, 'r', encoding='utf8').read()

txt = read_file(FILENAME)

features = {1:r'\b[A-Z]\w*\b'}

#pattern = '[A-ZŠĐČĆŽ]\w+'
for num, feature in features.items():
    for m in re.findall(feature, txt):
        print(num, repr(m))



