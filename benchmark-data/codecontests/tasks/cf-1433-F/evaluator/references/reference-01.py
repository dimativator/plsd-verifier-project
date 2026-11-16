import sys, math
import io, os
#data = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
#from bisect import bisect_left as bl, bisect_right as br, insort
#from heapq import heapify, heappush, heappop
from collections import defaultdict as dd, deque, Counter
#from itertools import permutations,combinations
def data(): return sys.stdin.readline().strip()
def mdata(): return list(map(int, data().split()))
def outl(var) : sys.stdout.write('\n'.join(map(str, var))+'\n')
def out(var) : sys.stdout.write(str(var)+'\n')
#from decimal import Decimal
#from fractions import Fraction
#sys.setrecursionlimit(100000)
INF = float('inf')
mod = int(1e9)+7


n,m,k=mdata()
A=[mdata() for i in range(n)]
dp1=[-INF]*k
dp1[0]=0
for i in range(n):
    dp=[[-INF]*(m//2+1) for _ in range(k)]
    dp[0][0]=0
    for j in range(m):
        a=A[i][j]
        for x in range(m // 2,0,-1):
            for y in range(k):
                dp[(y+a)%k][x]=max(dp[(y+a)%k][x],dp[y][x-1]+a)
    dp2=dp1[::]
    for x in range(k):
        for y in range(k):
            dp2[(x+y)%k]=max(dp2[(x+y)%k],dp1[x]+max(dp[y]))
    dp1=dp2[::]
out(dp1[0])