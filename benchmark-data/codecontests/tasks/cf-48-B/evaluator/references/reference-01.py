n, m = map(int, input().split())
t = [[0] * (m + 1)] + [[] for i in range(n)]
t[1] = [0] + list(map(int, input().split()))
for j in range(2, m + 1): t[1][j] += t[1][j - 1]
for i in range(2, n + 1):
    t[i] = [0] + list(map(int, input().split()))
    for j in range(2, m + 1): t[i][j] += t[i][j - 1]
    for j in range(1, m + 1): t[i][j] += t[i - 1][j]
a, b = map(int, input().split())
if a <= n and b <= m:
    p = min(t[i + a][j + b] + t[i][j] - t[i + a][j] - t[i][j + b] for i in range(n - a + 1) for j in range(m - b + 1))
a, b = b, a
if a <= n and b <= m:
    q = min(t[i + a][j + b] + t[i][j] - t[i + a][j] - t[i][j + b] for i in range(n - a + 1) for j in range(m - b + 1))
    if b <= n and a <= m: p = min(p, q)
    else: p = q
print(p)