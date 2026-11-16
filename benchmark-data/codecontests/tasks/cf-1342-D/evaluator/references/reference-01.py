import sys
from collections import defaultdict
from bisect import bisect_left
input = sys.stdin.readline
'''
n, m = map(int, input().split())
n = int(input())
A = list(map(int, input().split()))
S = input().strip()
for CASES in range(int(input())):
'''
inf = 100000000000000000  # 1e17
mod = 998244353

'''
# example input


'''
n, k = map(int, input().split())
A = sorted(map(int, input().split()), reverse=True)
C = list(map(int, input().split()))
ANS = [[] for i in range(n)]
SIZE = [0] * (n)
for a in A:
    require = C[a - 1]
    x = bisect_left(SIZE, -require + 1)
    SIZE[x] -= 1
    ANS[x].append(a)
print(bisect_left(SIZE, 0))
for ans in ANS:
    if len(ans) == 0:
        break
    print(len(ans), end=" ")
    print(*ans)
