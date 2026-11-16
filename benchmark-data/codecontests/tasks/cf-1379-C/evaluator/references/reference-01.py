from sys import stdin
import math
from bisect import bisect_right

input = stdin.readline
for _ in range(int(input())):

    n, m = map(int, input().split(" "))
    a = []
    xs = []
    ans = 0
    for i in range(m):
        x, y = map(int, input().split(" "))
        a.append((y, x))
        xs.append(x)
    garbage = input()
    xs.sort(reverse=True)
    a.sort(reverse=True)
    pos = 0
    s = 0
    l = 0
    for i in range(m):
        total = n - l
        y = a[i][0]
        while total and pos < m and y < xs[pos]:
            total-=1
            s += xs[pos]
            pos += 1
            l+=1

        if total:
            ans = max(ans, s+min(a[i])+(a[i][0]*(total-1)))
        else:
            ans = max(ans, s)
    print(ans)
