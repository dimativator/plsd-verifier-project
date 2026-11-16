from sys import stdin,setrecursionlimit
import threading
input = lambda: stdin.readline().rstrip("\r\n")
from collections import deque as que
inin = lambda: int(input())
inar = lambda: list(map(int,input().split()))
from types import GeneratorType


def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

    return wrappedfunc

from collections import defaultdict
adj=defaultdict(list)
visited=[False]*(100001)
intime=[0]*(100001)
outtime=[0]*(100001)
res=[]
bridge=False
timer=0
@bootstrap
def dfs(node,par):
    global adj, visited, intime, outtime, res, bridge,timer
    visited[node]=True
    intime[node]=timer
    outtime[node]=timer
    timer+=1
    for j in adj[node]:
        if j==par:
            continue
        if visited[j]:
            outtime[node]=min(outtime[node],intime[j])
            if intime[node]>intime[j]:
                res.append((node,j))
        else:
            yield dfs(j,node)
            if outtime[j]>intime[node]:
                bridge=True
                yield None
 
            res.append((node,j))
            outtime[node] = min(outtime[node], outtime[j])
    yield
def main():
    n,m=map(int,input().split())
    global adj,visited,intime,outtime,res,bridge,timer
    timer=0
    bridge=False
    for i in range(m):
        u,v=map(int,input().split())
        adj[u].append(v)
        adj[v].append(u)
    dfs(1,-1)
    if bridge:
        print(0)
    else:
        for i in range(len(res)):
            print(*res[i])

main()