n=int(input())
arr1=[int(c) for c in input().split()]
arr2=[int(c) for c in input().split()]

dic1={}
dic2={}

for i in range(n):
    dic1[arr1[i]] = i
    dic2[arr2[i]] = i

lshift=[0 for i in range(n)]
rshift=[0 for i in range(n)]

lcount={}
rcount={}

for i in range(n):
    dig=arr1[i]
    ind=dic2[dig]
    if ind <= i :
        lsh=(i-ind)
    else:
        lsh=i+(n-ind)
    
    if ind >= i :
        rsh=(ind-i)
    else:
        rsh=ind +n-i

    lshift[i] = lsh
    rshift[i] = rsh
    

for i in range(n):
    lcount[lshift[i]] = lcount.get(lshift[i],0) + 1
    rcount[rshift[i]] = rcount.get(rshift[i],0) + 1

ans=1

for i in lcount.keys():
    ans=max(ans,lcount[i])
for i in rcount.keys():
    ans=max(ans,rcount[i])

print(ans)