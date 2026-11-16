m,n=map(int,input().split())
a=[]
for i in range(m):
    p=[int(j) for j in input().split()]
    a.append(p)
  
for j in range(1,m):
    a[j][0]+=a[j-1][0]

for i in range(1,n):
    a[0][i]+=a[0][i-1]
    #print(a)
    for j in range(1,m):
        a[j][i]+=max(a[j-1][i],a[j][i-1])
        
#print(a) 
for i in range(m):
    p=int(a[i][n-1])
    print(p)