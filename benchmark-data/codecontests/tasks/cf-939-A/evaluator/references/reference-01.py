n=int(input())
a=list(map(int,input().split()))
for i in range(n):
     if a[a[a[i]-1]-1]==i+1:
         print('YES')
         exit(0)
print('NO')
