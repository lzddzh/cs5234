import matplotlib.pyplot as plt
import os

#os.system('python plot.py 1 > l1.txt')
#os.system('python plot.py 6 > l6.txt')

fre1 = []
fre2 = []
for each in open('l1.txt'):
    fre1.append(int(each.strip())/30000.0)
for each in open('l6.txt'):
    fre2.append(int(each.strip())/30000.0)

plt.ylabel('frequency')
plt.xlabel('words in book')
plt.plot(fre1, label="level1")
#plt.plot(fre2, label="level6")
plt.legend()
plt.show()
