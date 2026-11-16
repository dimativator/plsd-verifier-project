n, m = [int(x) for x in input().split()]
lr = []
lc = []
lst = []
for i in range(n):
    l = list(input())
    lr.append(l)
for i in range(m):
    l = []
    for j in range(n):
        s = lr[j][i]
        l.append(s)
    lc.append(l)
for i in range(n):
    for j in range(m):
        s = lr[i][j]
        if lr[i].count(s) == 1 and lc[j].count(s) == 1:
            lst.append(s)
print("".join(lst))