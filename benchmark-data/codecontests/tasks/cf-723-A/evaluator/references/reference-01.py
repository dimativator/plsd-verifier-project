a=list(map(int,input().split()))
a.sort()
if len(a)%2!=0:
    s=a[int(len(a)/2)]
    count=0
    for x in a:
        count+=abs(x-s)
    print(count)
 