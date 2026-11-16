h = int(input())
a = list(map(int, input().split()))
p, c, f = 0, 0, False
s1, s2 = [], []
for i in a:
    for j in range(i):
        s1.append(c)
        if j==i-1 and not f and p>=2 and i>=2:
            f = True
            s2.append(c-1)
        else:
            s2.append(c)
    p = i
    c += i
print('perfect' if not f else 'ambiguous')
if f:
    print(' '.join(map(str, s1)))
    print(' '.join(map(str, s2)))
#not the same
