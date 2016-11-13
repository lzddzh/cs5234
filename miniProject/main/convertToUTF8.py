import os 
import re
import sys

Dir = "/home/jayd/Desktop/NUS/Combinatorial and Graph Algorithms/miniProject"
# load book names in sub dir.
subDirs = os.listdir(Dir)
subDirs = sorted(subDirs)
booksName = []
booksDir = []
for d in subDirs:
    if d[:5] == 'level':
        booksName.extend(os.listdir(Dir + '/' +  d))
        for name in os.listdir(Dir + '/' + d):
            booksDir.append(d + '/' + name)

for each in booksDir:
    f = open(each, 'r')
    content = f.read()
    f.close()
    f = open(each, 'w')
    f.write(content.decode('gbk').encode('utf-8'))

