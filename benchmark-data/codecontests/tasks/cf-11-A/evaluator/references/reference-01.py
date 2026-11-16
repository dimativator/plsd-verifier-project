n,d=map(int,input().split())
l=[int(i) for i in input().split()]
s=0
import math 
for i in range(1,n):
    if l[i]>l[i-1]: 
        continue
    
    diff=l[i-1]-l[i]+1 
    
    s+=math.ceil(diff/d)
    l[i]+=d*math.ceil(diff/d)
print(s)