INF = 10 ** 13

h, n = map(int, input().split())
a = list(map(int, input().split()))
b = a[:]
for i in range(1, n):
    b[i] += b[i - 1]
low = min(b)
tot = b[-1]

if h + low <= 0:
    lo = 0
else:
    lo, hi = 0, INF
    while lo < hi:
        mid = (lo + hi) // 2
        cur = h + mid * tot + low
        if cur <= 0:
            hi = mid
        else:
            lo = mid + 1
if lo == INF:
    print(-1)
else:
    steps = lo * n
    cur = h + lo * tot
    for i in range(n):
        cur += a[i]
        steps += 1
        if cur <= 0:
            break
    print(steps)