import os 
import re
import sys
import matplotlib.pyplot as plt

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
fre1 = []
fre2 = []
for eachword in re.findall(r"[a-zA-Z]+", open(booksDir[41]).read().lower()):
    print eachword
    #answer = raw_input()
    #fre1.append(int(answer))
    #os.system("./fakeysyprog " + eachword)

#for eachword in re.findall(r"[a-zA-Z]+", open(booksDir[-1]).read().lower()):
    #print eachword
    #answer = raw_input()
    #fre2.append(int(answer))
    #os.system("./fakeysyprog " + eachword)
print 'done!'
#plt.ylabel('frequency')
#plt.xlabel('words in book')
#plt.plot(fre1, label="level1")
#plt.plot(fre2, label="level6")
#plt.legend()
#plt.show()
