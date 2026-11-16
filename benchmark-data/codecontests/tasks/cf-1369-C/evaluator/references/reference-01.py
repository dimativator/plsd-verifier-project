import sys 
input = lambda:sys.stdin.readline().strip()
t = int(input())
while t:
    t-=1
    n,k = map(int,input().split())
    a = list(map(int,input().split()))
    w = list(map(int,input().split()))
    adj = [[] for _ in range(k)]
    a.sort()
    w.sort()
    i = 0
    for i in range(k):
        adj[i].append(a.pop())
        w[i]-=1
    for i in range(k):
        while w[i]>0:
            adj[i].append(a.pop())
            w[i]-=1
    ans = 0
    for i in range(k):
        ans+=min(adj[i])+max(adj[i])
    print(ans)