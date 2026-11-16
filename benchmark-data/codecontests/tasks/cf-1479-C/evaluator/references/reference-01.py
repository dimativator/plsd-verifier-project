import sys
input = sys.stdin.readline
l,r=map(int,input().split())
dif=r-l+1
print("YES")
n=2
while 2**(n-2)<dif:n+=1
edges=[]
for i in range(n-2):
    for j in range(i+1,n-1):
        if i==0:
            edges.append([1,j+1,1])
        else:
            edges.append([i+1,j+1,2**(i-1)])
mx=l-1
i=1
if mx==0 or dif==2**(n-2):
    edges.append([1,n,mx+1])
    mx+=1
    dif-=1
while dif:
    if dif%2:
        edges.append([i+1,n,mx])
        mx+=2**(i-1)
    dif//=2
    i+=1
print(n,len(edges))
for e in edges:
    print(*e)