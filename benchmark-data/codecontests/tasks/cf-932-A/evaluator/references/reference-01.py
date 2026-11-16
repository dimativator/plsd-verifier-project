# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 21:01:05 2018

@author: DNARNAprotein
"""

"""
CODEFORCES
http://codeforces.com/contest/932/problem/A
"""

def pikachu(a,c,n): #c is original string
    prefixes=[a[0:i+1] for i in range(n+1)]
    suffixes=[a[i:n+1] for i in range(n+1)]
    maxi=0
    for i in range(n//2):
        for j in suffixes:
            if prefixes[i]==j:
                maxi=i+1
    ans=c[maxi::][::-1]+c
    l=len(ans)
    return ((ans,l))
    
a=input()
c=a
b=a[::-1]+'#'+a
a=a+'#'+a[::-1]

n=len(c*2)
x=pikachu(a,c,n)
c=c[::-1]
y=pikachu(b,c,n)
if x[1]<y[1]:
    print(x[0])
else:
    print(y[0])