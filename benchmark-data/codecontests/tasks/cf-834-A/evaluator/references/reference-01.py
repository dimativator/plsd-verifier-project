
a, b = input().split()
t = int(input())

d = dict()
d["^"] = 0
d[">"] = 1
d["v"] = 2
d["<"] = 3

a, b = d[a], d[b]
t = t % 4
if t == 2 or t == 0:
    print("undefined")
else:
    if t == 1:
        if (b-1) % 4 == a:
            print("CW".lower())
        else:
            print("CCW".lower())
    elif t == 3:
        if (b+1) % 4 == a:
            print("CW".lower())
        else:
            print("CCW".lower())


