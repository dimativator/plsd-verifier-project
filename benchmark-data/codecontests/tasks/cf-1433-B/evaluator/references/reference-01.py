import sys
try:
    import os
    f = open('input.txt', 'r')
    sys.stdin = f
except FileNotFoundError:
    None
from math import sqrt, ceil
input=lambda: sys.stdin.readline().strip()

o=int(input())
for _ in range(o):
    n=int(input())
    A=list(map(int,input().split()))
    dou=-1 ;las=-1
    for i in range(n):
        if dou==-1 and A[i]==1:
            dou=i
        if A[i]==1:
            las=i
    l= A[dou:las+1]
    print(l.count(0))
