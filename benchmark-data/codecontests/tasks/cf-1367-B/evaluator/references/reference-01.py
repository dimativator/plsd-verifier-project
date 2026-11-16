# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:21:12 2020

@author: user
"""
def solve(n,l):
    c1=0
    c2=0
    for i in range(n):
        if(i%2==0 and l[i]%2!=0):
            c1+=1
        elif(i%2!=0 and l[i]%2==0):
            c2+=1
    if(c1==c2):
        print(c1)
    else:
        print(-1)
            
t=int(input())
for i in range(t):
    n=int(input())
    l=list(map(int,input().split()))
    solve(n,l)