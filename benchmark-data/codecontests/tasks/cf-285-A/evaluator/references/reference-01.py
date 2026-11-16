n,k = map(int,input().strip().split())
a=list(range(1,n+1))
a[:k+1] = a[k::-1]
a=[str(i) for i in a]
print(' '.join(a))