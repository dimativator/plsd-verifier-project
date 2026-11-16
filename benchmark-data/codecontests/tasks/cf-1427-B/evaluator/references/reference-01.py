from functools import reduce
import os
import sys
from collections import *
#from fractions import *
from math import *
from bisect import *
from heapq import *
from io import BytesIO, IOBase
input = lambda: sys.stdin.readline().rstrip("\r\n")
def value(): return tuple(map(int, input().split())) # multiple values
def arr(): return [int(i) for i in input().split()] # array input
def sarr(): return [int(i) for i in input()] #array from string
def starr(): return [str(x) for x in input().split()] #string array
def inn(): return int(input()) # integer input
def svalue(): return tuple(map(str, input().split())) #multiple string values
def parr(): return [(value()) for i in range(n)] # array of pairs
mo = 1000000007
inf=1e18
div=998244353
#print("Case #{}:".format(_+1),end=" ")
# ----------------------------CODE------------------------------#
for _ in range(inn()):
    n,k=value()
    a=[str(x) for x in input()]
    ans=0
    c=0
    if(len(set(a))==1 and a[0]=='L'):
        print(max(0,k*2-1))
        continue
    for i in range(n):
        if(a[i]=='W'):
            if(i>0 and a[i-1]=='W'):
                ans+=2
            else:
                ans+=1
        else:
            c+=1
    i=0
    while(i<n and a[i]=='L'):
        i+=1
    j=n-1
    while(j>=0 and a[j]=='L'):
        j-=1
    res=[]
    while(i<j):
        val=i
        while(i<j and a[i]=='L'):
            i+=1
        if(i-val>0):
            res+=[i-val]
        else:
            i+=1
    res.sort()
    #print(res,c)
    for i in res:
        if(i>k):
            break
        ans+=(i*2+1)
        k-=i
        c-=i
    ans+=min(c,k)*2
    #print(c,k)
    print(min((n-1)*2+1,ans))





