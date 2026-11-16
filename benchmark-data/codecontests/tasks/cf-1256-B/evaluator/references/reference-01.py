def fn(n,a):
    v=[False]*n
    for i in range(1,n+1):
        c=a.index(i)-1
        while(c>=0):
            if(a[c]>a[c+1] and v[c]==False):
                v[c]=True
                a[c],a[c+1]=a[c+1],a[c]
            c=c-1
    return " ".join(str(x) for x in a)
m=int(input())
for i in range(m):
    n=int(input())
    a=[int(x) for x in input().split()]
    print(str(fn(n,a)))
            

        
