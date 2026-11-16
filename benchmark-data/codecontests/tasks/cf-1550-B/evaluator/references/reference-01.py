for iii in range(int(input())):
    n,a,b=map(int,input().split())
    q=input()
    if b>=0:
        x=n*(a+b)
        print(x)
    else:
        cout=1
        x=q[0]
        for i in range(1,n):
            if x!=q[i]:
                cout+=1
                x=q[i]
        print((n*a)+(((cout//2)+1)*b))
