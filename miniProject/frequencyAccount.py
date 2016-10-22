import os
import re
from collections import Counter
import matplotlib.pyplot as plt

# remove the dumplicated element in a list without change its order.
def removeDump(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

Dir = "/home/jayd/Desktop/NUS/Combinatorial and Graph Algorithms/miniProject"

# load the 10000 most frequenly used words sorted by frequency.
mostFreqWord = []
with open('10000frequentlyUsedVocabulary.txt') as f:
    for line in f:
        mostFreqWord.append(line.strip().split()[0])
    mostFreqWord = mostFreqWord[1:]
#mostFreqWord = removeDump(mostFreqWord)
dumItems = [item for item, count in Counter(mostFreqWord).items() if count > 1]
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
print str(len(booksName)) + ' books found in the directory.'

def countFre2(fileDir):
    # Replace all non-alpha characters by a space.
    # All text to lower case.
    words = re.findall(r"[a-zA-Z]+", open(fileDir).read().lower())
    c = Counter(words)
    fre = []
    total = 0.0
    i = 0
    firstHalf = 0.0
    for e in mostFreqWord:
        if i == 5000:
            firstHalf = total
            total = 0
        fre.append(c[e]/(len(words) + 0.0))
        total += c[e]
        i = i + 1 
    return firstHalf/(len(words) + 0.0), total/(len(words) + 0.0)


def countFre(fileDir):
    # Replace all non-alpha characters by a space.
    # All text to lower case.
    words = re.findall(r"[a-zA-Z]+", open(fileDir).read().lower())
    print len(words)
    c = Counter(words)
    fre = []
    total = 0.0
    for e in mostFreqWord:
        fre.append(c[e]/(len(words) + 0.0))
        total += c[e]
    return fre, total/len(words)

fre1, o1 = countFre(Dir + '/' + booksDir[0])
fre2, o2 = countFre(Dir + '/' + booksDir[-1])
fir1, sec1 = countFre2(Dir + '/' + booksDir[0])
fir2, sec2 = countFre2(Dir + '/' + booksDir[-1])
for i in range(0, len(fre1)):
    if fre1[i] > 0.01:
        fre1[i] = 0.01
for i in range(0, len(fre2)):
    if fre2[i] > 0.01:
        fre2[i] = 0.01
plt.ylabel('frequency')
plt.xlabel('5000 words')
plt.plot(fre1, label=booksDir[0][:6])
plt.plot(fre2, label=booksDir[-1][:6])
plt.legend()

for b in booksDir:
    fre, o = countFre(Dir + '/' + b)
    fir, sec = countFre2(Dir + '/' + b) 
    print "with in the vocabulary list: " + str(o) + "  first half: " + str(fir) + "   second half: " + str(sec)

plt.show()
