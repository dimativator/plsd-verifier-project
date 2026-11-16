n, m = map(int, input().split())
print(max(n-2*m, 0), end=' ')
for i in range(0, n+1):
    if i*(i-1)/2>=m: break
print(n-i)