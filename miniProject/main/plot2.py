import matplotlib.pyplot as plt
import os
import numpy as np

#os.system('python plot.py 1 > l1.txt')
#os.system('python plot.py 6 > l6.txt')

fre1 = []
fre2 = []
fre3 = []
fre4 = []
fre5 = []
fre6 = []
for each in open('l1.txt'):
    fre1.append(int(each.strip()))
for each in open('l2.txt'):
    fre2.append(int(each.strip()))
for each in open('l3.txt'):
    fre3.append(int(each.strip()))
for each in open('l4.txt'):
    fre4.append(int(each.strip()))
for each in open('l5.txt'):
    fre5.append(int(each.strip()))
for each in open('l6.txt'):
    fre6.append(int(each.strip()))

print np.var(fre1), np.var(fre2), np.var(fre3), np.var(fre4), np.var(fre5), np.var(fre6)

print np.mean(fre1), np.mean(fre2),np.mean(fre3),np.mean(fre4),np.mean(fre5),np.mean(fre6)

