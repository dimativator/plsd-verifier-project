n=int(input())
l=input()
e=[]
p=0
for i in l:
    if i=='(':
        p+=1
        e.append(p)
    else:
        p-=1
        e.append(p)
if e[-1]!=0:
    print(-1)
else:
    ans=0
    z=0
    for i in range(n):
        if e[i]<0:
            z+=1
        else:
            if z>0:
                ans+=z+1
                z=0
    print(ans)

