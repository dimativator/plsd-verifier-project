from sys import *
input = stdin.readline

n,k = map(int,input().split())
graph = [set([]) for _ in range(n+1)]

for _ in range(n-1):
    x,y = map(int,input().split())
    graph[x].add(y)
    graph[y].add(x)

dep,par,cn = [0]*(n+1),[0]*(n+1),0
q,p = [1],[]
vis = [0]*(n+1)
vis[1] = 1

while(q):
    x = q.pop()
    dep[x] = cn
    for i in graph[x]:
        if(vis[i] == 0):
            vis[i] = 1
            p.append(i)
            par[i] = x
    if(len(q) == 0):
        cn += 1
        q = list(p)
        p = []
    
tp = []
for i in range(1,n+1):
    tp.append((i,dep[i]))
tp.sort(key = lambda x : (x[1]))
tp = tp[::-1]

sub = [0]*(n+1)
for i in range(len(tp)-1):
    ind = tp[i][0]
    pid = par[ind]
    sub[pid] += 1 + sub[ind]

a = []
for i in range(1,n+1):
    a.append(dep[i]-sub[i])
a.sort(reverse = True)

sn = 0
for i in range(k):
    sn += a[i]

stdout.write(str(sn)+'\n')