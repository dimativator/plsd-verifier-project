
for _ in range(int(input())):
    n,k=map(int,input().split())
    d=dict()
    a=[]
    new=[]
    for x in input().split():
        x=int(x)
        a.append(x)
        if x not in d:
            d[x]=0
            new.append(x)
        d[x]+=1
    if len(d)>k:
        print("-1")
    else:
        while len(new)!=k:
            new.append(new[-1])
        print(n*k)
        for i in range(n):
            print(*new[:k],end=" ")
        print("")
        