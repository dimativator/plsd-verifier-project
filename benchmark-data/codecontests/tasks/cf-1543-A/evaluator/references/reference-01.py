import io,os
input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

import math
t=int(input())
while(t>0):
    t-=1
    a,b=sorted(list(map(int,input().split())))
    if(a==0):
        print(str(b)+" 0")
        continue
    if(a==b):
        print("0 0")
        continue
    if((b-a)==1):
        print("1 0")
        continue
    else:
        g=b-a
        
        print(str(g)+" "+str(min(b%g,g-b%g)))