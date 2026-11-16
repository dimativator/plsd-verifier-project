import sys
import math as mt
input=sys.stdin.buffer.readline  
#t=int(input())
t=1
for __ in range(t):
    #n=int(input())
    n,k=map(int,input().split())
    
    l=list(map(int,input().split()))
    l.sort()
    maxn,maxl=l[0],1
    suma=[0]*(n+2)
    suma[0]=0
    for i in range(n):
        suma[i+1]=suma[i]+l[i]
    to=0
    for i in range(1,n):
        while((i-to)*l[i]-(suma[i]-suma[to]))>k:
            to+=1
        if maxl<i-to+1:
            maxl=i-to+1
            maxn=l[i]
            
    print(maxl,maxn)    