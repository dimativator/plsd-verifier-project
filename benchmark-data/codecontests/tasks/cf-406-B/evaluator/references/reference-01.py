import sys
INF = 10**20
MOD = 10**9 + 7
I = lambda:list(map(int,input().split()))
from math import gcd
from math import ceil
from collections import defaultdict as dd, Counter
from bisect import bisect_left as bl, bisect_right as br


"""
Facts and Data representation
Constructive? Top bottom up down
"""
n, = I()
a = I()
M = 10 ** 6 + 1
take = [0] * M
for i in a:
  take[i] = 1

ans = []
ok = []
cnt = 0
for i in range(1, M // 2 + 1):
  if take[i] and take[M - i]:
    cnt += 1
  elif not take[i] and not take[M - i]:
    ok.append((i, M - i))
  elif take[i]:
    ans.append(M - i)
  else:
    ans.append(i)

for i in range(cnt):
  ans.append(ok[i][0])
  ans.append(ok[i][1])

print(len(ans))
print(*ans)