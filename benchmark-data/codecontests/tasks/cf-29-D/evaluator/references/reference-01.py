n = int(input())
adj = [[] for i in range(n)]
adj2 = [[] for i in range(n)]
for i in range(n-1):
    u,v = map(int,input().split())
    adj[u-1].append(v-1)
    adj[v-1].append(u-1)

leaf = {}
a = list(map(int,input().split()))
for i in range(len(a)):
    leaf[a[i]-1] = i
inf = 200000
def dfs1(v,frm,adj2):
    if len(adj[v]) == 1 and v!=0:
        return (inf if v not in leaf else leaf[v],v)
    best = float("inf")
    for u in adj[v]:
        if u != frm:
            c = dfs1(u,v,adj2)
            adj2[v].append(c)
            best = min(best,c[0])
    return (best,v)

dfs1(0,-1,adj2)            
path = []
for i in range(n):
    adj2[i].sort()
#print(*adj2)
def dfs2(v,frm,path):
    path.append(v+1)
    for _,u in adj2[v]:
        if u!=frm:
            dfs2(u,v,path)
    if frm!=-1:
        path.append(frm+1)            
dfs2(0,-1,path)
gd = []
for i in path:
    if i-1 in leaf:
        gd.append(i)

if gd == a:
    print(*path)
else:
    print(-1)
