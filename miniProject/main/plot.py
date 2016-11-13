f = open("The Monkey's Paw.txt")
content = f.read()
lines = content.strip().split();
num = [int(x) for x in lines]

array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for each in num:
    array[each] += 1
s = 0
for each in array:
    s += each
for i in range(0, len(array)):
    array[i] = (array[i] + 0.0) / s 
print s, array
