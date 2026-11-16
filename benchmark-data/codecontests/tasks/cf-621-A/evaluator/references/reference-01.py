n=int(input())
l=list(map(int,input().split()))
s=sum(l)
ls=set(l)
lss=list(ls)
lss.sort()
c=0
for i in range(len(lss)):
    if lss[i]%2!=0:
        c=lss[i]
        break
if s%2==0:
    print(s)
else:
    
    print(s-c)