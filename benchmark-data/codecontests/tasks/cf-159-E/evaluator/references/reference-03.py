import sys
n = int(sys.stdin.readline())
cube = dict()
for i in xrange(n):
    c, s = map(int, sys.stdin.readline().split())
    if c not in cube:
        cube[c] = []
    cube[c].append( (s, i) )
m = 0
cube = [cube[x] for x in cube]
cs = []
for x in cube:
    x.sort()
    x.reverse()
    s = [0]
    for i in x:
        s.append(s[-1] + i[0])
    cs.append(s)
    m = max(len(x), m)

n_used = [[[0, 1010101]]]
for k in xrange(1, m+1):
    tmp = [[0, 1010101]]
    for i in xrange(len(cube)):
        if len(cube[i]) < k:
            continue
        tmp.append([cs[i][k], i])
        tmp.sort()
        tmp.reverse()
        if len(tmp) > 2:
            tmp = tmp[:2]
    n_used.append(tmp)
n_used.append([[0, 1010101]])
#print n_used
ans = 0
p = q = 0
for i in xrange(len(cube)):
    x = cube[i]
    a = n_used[len(x) + 1]
    j = 1 if a[0][1] == i else 0
    if a[j][0] and ans < cs[i][-1] + a[j][0]:
        ans = cs[i][-1] + a[j][0]
        p = x[:]
        q = cube[a[j][1]][:len(x) + 1]
    a = n_used[len(x)]
    j = 1 if a[0][1] == i else 0
    if a[j][0] and ans < cs[i][-1] + a[j][0]:
        ans = cs[i][-1] + a[j][0]
        p = x[:]
        q = cube[a[j][1]][:len(x)]
print ans
print len(p) + len(q)
for (i, j) in zip(p, q):
    print j[1]+1, i[1]+1,
if len(p) < len(q):
    print q[-1][1]+1
