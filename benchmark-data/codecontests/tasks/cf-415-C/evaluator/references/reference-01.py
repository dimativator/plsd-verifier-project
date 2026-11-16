n,k=map(int,input().split())
if n//2>k or (k!=0 and n==1):
    print(-1)
    exit(0)
ans=[0]*n
ans[0]=k-n//2+1
if n>1:
    ans[1]=2*ans[0]
    for i in range(2,n):
        ans[i]=ans[i-1]+1
print(*ans)