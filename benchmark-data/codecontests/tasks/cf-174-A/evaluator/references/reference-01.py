a,b=map(int,input().split())
l=list(map(int,input().split()))
if (max(l)*a)-sum(l)>b:
    print(-1)
else:
    for i in l:
        print((sum(l)+b)/a-i)