from collections import deque
from sys import stdin
import sys

tt = int(stdin.readline())

for loop in range(tt):

    n = int(stdin.readline())

    lis = [ [] for i in range(2**n)]

    for i in range(n*(2**(n-1))):

        u,v = map(int,stdin.readline().split())
        lis[u].append(v)
        lis[v].append(u)

    rp = [0] * (2**n)
    d = [float("inf")] * (2**n)

    d[0] = 0

    q = deque()
    for i in range(n):
        nexv = lis[0][i]
        rp[nexv] = 2**i
        d[nexv] = 1
        q.append(nexv)

    while q:
        v = q.popleft()
        for nexv in lis[v]:

            if d[nexv] == float("inf"):
                d[nexv] = d[v] + 1
                q.append(nexv)

            if d[nexv] > d[v]:
                rp[nexv] |= rp[v]

    p = [None] * (2**n)
    for i in range(2**n):
        p[rp[i]] = i

    print (*p)

    if (2**n) % n == 0:

        c = [None] * (2**n)
        
        for i in range(2**n):

            now = 0
            for j in range(n):
                if 2**j & i > 0:
                    now ^= j
            c[p[i]] = now

        print (*c)

    else:
        print (-1)
                