n=int(input())
a=list(map(int,input().split()))
i=0
temp=0
for i in range(n//2):
    if i%2==0:
        temp=a[i]
        a[i]=a[n-i-1]
        a[n-i-1]=temp
for r in a:
    print(r,end=' ')