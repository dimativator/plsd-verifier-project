from collections import defaultdict
import sys
from sys import stdin
def check(a):
    for i in a:
        if i:
            return True
    return False
def change(x):
    return ord(x)-ord('a')  
def solve():
    n, m = map(int, stdin.readline().split())
    s = input()
    d = {}
    for i in range(n):
        d[i+1] = s[i]
    g = defaultdict(list)#[[] for _ in range(n+1)]
    ind = [0 for _ in range(n+1)]
    for _ in range(m):
        x, y = map(int, stdin.readline().split())
        g[x].append(y)
        ind[y]+=1
    q = []
    dp = [[0 for _ in range(27)]for _ in range(n + 1)]
    for i in range(1, n+1):
        if ind[i]==0:
            q.append(i)
            dp[i][change(d[i])] = 1
    for i in q:
        for j in g[i]:
            for k in range(26):
                if change(d[j])==k:
                    dp[j][k] = max(dp[i][k]+1, dp[j][k])
                else:
                    dp[j][k] = max(dp[i][k], dp[j][k])
            ind[j]-=1
            if ind[j]==0: q.append(j)
    if check(ind):
        print(-1)
    else:
        ans = 0
        for i in dp:
            for j in i:
                ans = max(ans, j)
        print(ans)
t = 1   
#t = inp()
for _ in range(t):
    solve()
