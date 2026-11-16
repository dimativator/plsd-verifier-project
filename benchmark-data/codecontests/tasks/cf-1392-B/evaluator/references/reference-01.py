t=int(input())
for i in range(t):
    n,k=map(int,input().split())
    ar=list(map(int,input().split()))
    m=max(ar)
    new=[]
    for i in range(n):
        new.append(m-ar[i])
    if k%2==0:
        mx=max(new)
        for j in range(n):
            new[j]=mx-new[j]

    print(*new)
    
