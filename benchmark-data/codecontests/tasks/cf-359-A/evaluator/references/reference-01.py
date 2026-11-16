n,m=map(int,input().split())
l=[list(map(int,input().split())) for _ in range(n)]
for i in range(n):
    if (i==0 or i==n-1) and sum(l[i]): print(2); break
    elif l[i][0]==1 or l[i][-1]==1: print(2); break
else: print(4)
