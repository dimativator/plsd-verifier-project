n, d, L = map(int, input().split())
sp = []
for _ in range(n - 1):
    if d <= 0:
        sp.append(1)
        d = 1 - d
    else:
        sp.append(L)
        d = L - d
if 1 <= d <= L:
    sp.append(d)
    print(*sp)
else:
    print(-1)
