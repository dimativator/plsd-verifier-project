n=int(input())
a=[[0 for j in range(n)] for i in range(n)]
for i in range(n-1):
    for j in range(n-1):
        if i!=j:
            a[i][j]=(i+j)%n+int(i+j>=n)
    a[i][n-1]=((n-1+2*i)%n+int(n-1+2*i>=n))%n+int(n-1+2*i>2*(n-1))
for i in range(n-1):
    a[n-1][i]=((n-1+2*i)%n+int(n-1+2*i>=n))%n+int(n-1+2*i>2*(n-1))
for i in a:
    print(*i)