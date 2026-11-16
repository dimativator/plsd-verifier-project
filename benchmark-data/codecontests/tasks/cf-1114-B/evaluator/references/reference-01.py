from operator import itemgetter
from itertools import accumulate
from sys import stdin, stdout
n, m, k = [int(x) for x in stdin.readline().split()]
a = [int(x) for x in stdin.readline().split()]
id = [x for x in range(n)]
b = list(zip(a, id))
a.sort(reverse = True)
b.sort(reverse = True)
c = [p[1] for p in b[:m*k]]
c.sort()
print(list(accumulate(a[:m*k]))[-1])
for x in [x + 1 for x in c][m-1::m][:k-1]:
    print(x, end = ' ')