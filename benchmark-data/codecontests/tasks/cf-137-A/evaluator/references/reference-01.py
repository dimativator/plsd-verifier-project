import math
l = list(map(str, input()))
t = 0
while len(l) != 0:
    c = 0
    b = l[0]
    x = 1
    while True:
        if x == len(l):
            t += math.ceil(x / 5)
            l = []
            break
        elif b == l[x]:
            x += 1
        else:
            t += math.ceil(x/5)
            l = l[x:]
            break
print(t)