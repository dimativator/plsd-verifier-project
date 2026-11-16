n,m = map(int, input().split())
if n < m:
    print(-1)
else:
    if n % 2 == 0:
        b = n//2
    else:
        b = (n//2)+1
    while b % m != 0:
        b = b + 1
    print(b)