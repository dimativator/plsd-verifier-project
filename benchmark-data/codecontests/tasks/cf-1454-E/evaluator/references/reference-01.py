import sys
input=sys.stdin.readline
from collections import defaultdict,deque
t=int(input())
for _ in range(t):
    n=int(input())
    ct=[1]*(n+1)
    deg=[0]*(n+1)
    d=defaultdict(set)
    for _ in range(n):
        u,v=map(int,input().split())
        d[u].add(v)
        d[v].add(u)
        deg[u]+=1
        deg[v]+=1
    hp=deque()
    for i in range(n+1):
        if deg[i]==1:
            hp.append(i)
    while hp:
        x=hp.popleft()
        y=d[x].pop()
        d[y].remove(x)
        deg[y]-=1
        if deg[y]==1:
            hp.append(y)
        ct[y]+=ct[x]
        ct[x]=0
    ans=0
    for i in range(1,n+1):
        ans+=(ct[i]*(ct[i]-1))//2+ct[i]*(n-ct[i])   
        
    print(ans)