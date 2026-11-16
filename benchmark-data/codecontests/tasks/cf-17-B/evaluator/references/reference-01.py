import sys
import math
import collections
import heapq
input=sys.stdin.readline
n=int(input())
l=[int(i) for i in input().split()]
m=int(input())
s=0
d={}
for i in range(m):
    a,b,c=(int(i) for i in input().split())
    if(b in d):
        d[b]=min(d[b],c)
    else:
        d[b]=c
c1=0
for i in range(1,n+1):
    if(i not in d):
        c1+=1
if(c1>1):
    print(-1)
else:
    for i in d:
        s+=d[i]
    print(s)