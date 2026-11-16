from math import *
from collections import Counter,defaultdict,deque
I =lambda:int(input())
M =lambda:map(int,input().split())
LI=lambda:list(map(int,input().split()))


for _ in range(I()):
    n=I()
    s=input()
    dc=0
    kc=0
    d=defaultdict(int)
    for i in s:
        dc+=i=="D"
        kc+=i=="K"
        g=gcd(dc,kc)
        d[(dc//g,kc//g)]+=1
        print(d[(dc//g,kc//g)],end=" ")
    print()   
            

    



    

