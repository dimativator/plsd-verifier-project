n,m=map(int,input().split())
"""L=[]
for i in range(n):
    s=[]
    L.append(s)"""

dp=[]

for i in range(n-1):
    u,v,w=map(int,input().split())
    #L[u-1].append(v-1)
    #L[v-1].append(u-1)
    dp.append((w,u-1,v-1))
dp=sorted(dp)
q=[int(x) for x in input().split()]
pos=[]
for i in range(m):
    pos.append(i)

Q=sorted(zip(q,pos))

par=[]
for i in range(0,n):
    par.append(i)

rank=[1]*n

def find(x):
    if(par[x]!=x):
        par[x]=find(par[x])
    return par[x]


global res

res=0

def union(x,y):
    global res
    X=find(x)
    Y=find(y)

    if(rank[X]<rank[Y]):
        temp=X
        X=Y
        Y=temp

    res=res-(rank[X]*(rank[X]-1)//2)
    res=res-(rank[Y]*(rank[Y]-1)//2)
    rank[X]+=rank[Y]
    res=res+(rank[X]*(rank[X]-1)//2)
    par[Y]=X
    """if(X==Y):
        return
    if(rank[X]<rank[Y]):
        par[X]=Y
    elif(rank[X]>rank[Y]):
        par[Y]=X
    else:
        par[Y]=X
        rank[X]=rank[Y]+1"""

ans=[0]*m
ptr=0
for i in range(0,m):
    while(ptr<n-1 and dp[ptr][0]<=Q[i][0]):
        a=dp[ptr][1]
        b=dp[ptr][2]
        union(a,b)
        ptr+=1
    ans[Q[i][1]]=res
"""temp=Q[0][0]
ptr=0
for i in range(0,len(dp)):
    if(dp[i][0]>temp):
        ans[Q[ptr][1]]=res
        ptr+=1
        temp=Q[ptr][0]
    union(dp[i][1],dp[i][2])
for i in range(ptr,len(Q)):
    ans[Q[i][1]]=res"""
print(*ans)
