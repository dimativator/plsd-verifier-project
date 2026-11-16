n = int(input())
lis = list(map(int,input().split()))
pre=[0]*(n+1)
for i in range(1,n+1):
    pre[i]=pre[i-1]+lis[i-1]
if pre[-1]%3:
    print(0)
else:
    s=pre[-1]//3
    ans=t=0
    for i in range(1,n):
        if pre[i]==2*s:
            ans+=t
        if pre[i]==s:
            t+=1
    print(ans)                    