from collections import deque
from math import ceil,floor,sqrt,gcd
def ii(): return int(input())
def mi(): return map(int,input().split())
def li(): return list(mi())
def si():return input()
n=ii()
a=li()
m={}
for i in a:
    if i not in m:
        m[i]=1
    else:
        m[i]+=1
b=[]
for i in m.keys():
    b.append(m[i])
b.sort()
if(len(b)==3):
    print(b[0]+b[1])
elif(len(b)==2):
    print(b[0])
else:
    print('0')