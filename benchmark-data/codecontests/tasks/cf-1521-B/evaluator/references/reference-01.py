from sys import stdin
"""
n=int(stdin.readline().strip())
n,m=map(int,stdin.readline().strip().split())
s=list(map(int,stdin.readline().strip().split()))
"""
T=int(stdin.readline().strip())
for caso in range(T):
    n=int(stdin.readline().strip())
    s=list(map(int,stdin.readline().strip().split()))
    mn=10**20
    ind=-1
    for i in range(n):
        if s[i]<mn:
            ind=i
            mn=s[i]
    ans=[]
    t=True
    for i in range(ind+1,n):
        if t:
            ans.append([ind+1,i+1,mn,mn+1])
        else:
            ans.append([ind+1,i+1,mn,mn])
        t=not t
    t=True
    for i in range(ind-1,-1,-1):
        if t:
            ans.append([ind+1,i+1,mn,mn+1])
        else:
            ans.append([ind+1,i+1,mn,mn])
        t=not t
    print(len(ans))
    for i in ans:
        print(*i)
