from sys import stdin,stdout
n,k=map(int ,stdin.readline().strip().split())
if n==k:
    print(-1)
else:
    result=[0]*n
    for i in range(n-k,n):
        result[i]=i+1
    for i in range(1,n-k):
        result[i]=i
    result[0]=n-k
    print(*result,sep=' ')
        
