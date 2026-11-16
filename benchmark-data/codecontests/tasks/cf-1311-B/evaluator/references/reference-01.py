t=int(input())
for _ in range(t):
    n,m=map(int,input().split())
    a=list(map(int,input().split()))
    b=[(a[i],i) for i in range(n)]
    b=sorted(b)
    p=list(map(int,input().split()))
    adj=[[] for i in range(n)]
    for i in range(m):
        p[i]=p[i]-1
    for i in p:
        adj[i].append(i+1)
        adj[i+1].append(i)
    ok=True
    for i in range(n):
        q=[b[i][1]]
        temp=False
        while len(q) is not 0:
            s=q.pop(0)
            if s==i:
                temp=True
                break
            if i>s:
                if s+1 in adj[s]:
                    q.append(s+1)
                else:
                    break
            else:
                if s-1 in adj[s]:
                    q.append(s-1)
                else:
                    break
        if temp==False:
            ok=False
            break
    if ok==True:
        print("YES")
    else:
        print("NO")