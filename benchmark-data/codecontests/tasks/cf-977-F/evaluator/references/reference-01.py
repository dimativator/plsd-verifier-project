n=int(input())
l=list(map(int,input().split()))
d={}
dp=[0 for i in range(n)]
ind=dp[:]
dp[0]=1
d[l[0]]=0
for i in range(1,len(l)):
    if l[i]-1 in d:
        dp[i]=1+dp[d[l[i]-1]]
        ind[i]=d[l[i]-1]
    else:
        dp[i]=1
    d[l[i]]=i
print(max(dp))
i=dp.index(max(dp))
mx=max(dp)
ans=[]
while mx:
    ans.append(i+1)
    i=ind[i]
    mx-=1
print(*ans[::-1])
