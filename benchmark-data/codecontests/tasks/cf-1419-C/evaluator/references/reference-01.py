for _ in range(int(input())):
    n,x=map(int,input().split())
    a=list(map(int,input().split()))
    if len(set(a))==1 and list(set(a))[0]==x:
        print(0)
    elif sum(a)/n==x:
        print(1)
    elif x in a:
        print(1)
    else:
        print(2)