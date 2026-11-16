n,k=map(int,input().split())
s=input()
di=dict()
for i in s:di[i]=di.get(i,0)+1
ans=0
se=list(set(s))
se.sort(key=lambda x:di[x],reverse=1)
for i in se:
    ans+=min(k,di[i])*min(di[i],k)
    k-=min(di[i],k)
    if not k:break
print(ans)
