def swap_sum(a,b,cnt,k):
    if cnt==k or min(a)>=max(b):
        return sum(a)
        
        
    else:
        i=a.index(min(a))
        j=b.index(max(b))
        a[i],b[j]=b[j],a[i]
        #print(a)
        #print(b)
        return swap_sum(a,b,cnt+1,k)


for ii in range(int(input())):
    n,k=map(int,input().split())
    a=list(map(int,input().split()))
    b=list(map(int,input().split()))
    print(swap_sum(a,b,0,k))
    