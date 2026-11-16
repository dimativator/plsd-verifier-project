from typing import List
import sys
 
n, m = [int(a) for a in input().split(' ')]
 
adj: List[List[int]] = [[]] + [[] for _ in range(n)]
 
visited: List[bool] = [False] * (n + 1)
parent: List[int] = [0] * (n + 1)
depth: List[int] = [0] * (n + 1)
low: List[int] = [0] * (n + 1)
cx: List[int] = [0] * (n + 1)
cy: List[int] = [0] * (n + 1)
qi: List[int] = [0] * (n + 1)
 
for i in range(m):
    u, v = [int(a) for a in input().split(' ')]
    adj[u].append(v)
    adj[v].append(u)
 
 
def solve():
 
    for i in range(1, n + 1):
        if not visited[i]:
            # dfs(i)
            dfs2(i)
    print('NO')
 
 
def lca(a, b):
    while depth[a] > depth[b]:
        a = parent[a]
    while depth[b] > depth[a]:
        b = parent[b]
    while a != b:
        a = parent[a]
        b = parent[b]
    return a
 
 
def parent_path(a, b):
    p = []
    while a != b:
        p.append(str(a))
        a = parent[a]
    p.append(str(b))
    return p
 
 
def gett(a, b, u, v):
    if depth[b] > depth[v]:
        a, b, u, v = u, v, a, b
    e = lca(a, u)
    print('YES')
    c1 = parent_path(e, v)
    print(' '.join([str(len(c1))] + c1))
    c2 = list(reversed(parent_path(a, e))) + list(reversed(parent_path(v, b)))
    print(' '.join([str(len(c2))] + c2))
    c3 = list(reversed(parent_path(u, e))) + [str(v)]
    print(' '.join([str(len(c3))] + c3))
    exit(0)
 
 
def dfs(i):
    visited[i] = True
    depth[i] = depth[parent[i]] + 1
    for ni in adj[i]:
        if parent[i] != ni:
            if not visited[ni]:
                parent[ni] = i
                dfs(ni)
            elif depth[ni] < depth[i]:
                x = i
                while x != ni:
                    if cx[x] and cy[x]:
                        gett(cx[x], cy[x], i, ni)
                    else:
                        cx[x] = i
                        cy[x] = ni
                    x = parent[x]
 
 
def dfs2(i):
    visited[i] = True
    q: List[int] = []
    q.append(i)
    while len(q) > 0:
        u = q[-1]
        if qi[u] >= len(adj[u]):
            q.pop()
            continue
        v = adj[u][qi[u]]
        qi[u] += 1
        if parent[u] != v:
            if not visited[v]:
                parent[v] = u
                depth[v] = depth[u] + 1
                visited[v] = True
                q.append(v)
            elif depth[v] < depth[u]:
                x = u
                while x != v:
                    if cx[x] and cy[x]:
                        gett(cx[x], cy[x], u, v)
                    else:
                        cx[x] = u
                        cy[x] = v
                    x = parent[x]
 
solve()
