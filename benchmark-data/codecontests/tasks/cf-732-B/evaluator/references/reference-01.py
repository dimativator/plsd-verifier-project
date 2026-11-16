import math
n,k=map(int,input().split())
l2=[]
a=list(map(int,input().split()))
for i in a:
    l2.append(i)
i=1
l=[a[0]]
while i<=n-1:
    if a[i]+a[i-1]<k:
        a[i]=k-a[i-1]
        l.append(k-a[i-1])
    else:
        l.append(a[i])
    i=i+1
print(sum(l)-sum(l2))
print(*l)
