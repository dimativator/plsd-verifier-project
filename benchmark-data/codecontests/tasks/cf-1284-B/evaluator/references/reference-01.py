n=int(input())
l=[]
ans=0
minn=[]
maxx=[]
c=0
for _ in range(n):
    ar=[int(x) for x in input().split()]
    ar=ar[1:]
    m=10**10
    f=0
    for i in ar:
        if i<=m:
            m=i
        else:
            f=1
            break
    if f==1:
        continue
    else:
        minn.append(min(ar))
        maxx.append(max(ar))
maxx.sort()
minn.sort()
temp=len(maxx)
from bisect import bisect_left
for i in maxx:
    ind=bisect_left(minn,i)
    ans+=temp-ind
print(n**2-ans)