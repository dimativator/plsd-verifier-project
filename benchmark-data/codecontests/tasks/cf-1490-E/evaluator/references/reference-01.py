import sys
import math
input = sys.stdin.readline
mod=10**9+7
############ ---- Input Functions ---- ############
def inp():
    return(int(input()))
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input()
    return(list(s[:len(s) - 1]))
def invr():
    return(map(int,input().split()))
for _ in range(inp()):
    n=inp()
    l=inlt()
    x=[]
    for i in range(n):
        x.append([l[i],i+1])
    x.sort(key=lambda x:x[0])
    out=[]
    s=0
    a=[]
    y=0
    for i in range(n):
        s=s+x[i][0]
        a.append(s)
    for i in range(n-1):
        if a[i]<x[i+1][0]:
            y=i+1
    for i in range(y,len(x)):
        out.append(x[i][1])
    out.sort()
    print(len(out))
    print(" ".join(str(i) for i in out))
