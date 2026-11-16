n,v=map(int,input().split())
a=[int(i) for i in input().split()]
b=[int(i) for i in input().split()]
mini=10**9  
for i in range(n):
    mini=min(mini,b[i]/a[i])
sm=0 
for i in range(n):
    sm=sm+mini*a[i]
print(min(sm,v))