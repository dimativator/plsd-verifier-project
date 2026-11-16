import sys
input = sys.stdin.readline
from bisect import *

n = int(input())
ab = [tuple(map(int, input().split())) for _ in range(n)]
ab.sort(key=lambda k: k[0])
a = [-10**18]+[ai for ai, _ in ab]
dp = [0]*(n+1)

for i in range(1, n+1):
    j = bisect_left(a, ab[i-1][0]-ab[i-1][1])-1
    dp[i] = dp[j]+i-j-1

ans = 10**18

for i in range(n+1):
    ans = min(ans, dp[i]+n-i)

print(ans)