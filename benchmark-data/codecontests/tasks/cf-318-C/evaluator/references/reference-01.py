from sys import stdin
from math import ceil

x, y, m = map(int, stdin.readline().split())
ans = 0
if x >= m or y >= m:
    print(ans)
elif x + y > min(x, y):
    ma, mi = max(x, y), min(x, y)
    ans += ((ma - mi) // ma)  # + ((ma - mi) % ma)

    mi, ma = min(ma, mi + ans * ma), max(ma, mi + ans * ma)

    while ma < m:
        ma, mi = ma + mi, ma
        ans += 1

    print(ans)
else:
    print(-1)
