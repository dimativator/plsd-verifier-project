n = int(input())
a = [0] + [int(x) for x in input().split()]
b = [0] + [int(x) for x in input().split()]
q = [0 for i in range(n + 1)]
f = [0 for _ in range(n + 1)]
l, r, q[1] = 1, 1, 1
for i in range(2, n + 1):
    while l < r and f[q[l + 1]] - f[q[l]] < a[i] * (b[q[l]] - b[q[l + 1]]):
        l += 1
    f[i] = f[q[l]] + b[q[l]] * a[i]
    while l < r and (f[q[r]] - f[q[r - 1]]) * (b[q[r]] - b[i]) >= (f[i] - f[q[r]]) * (b[q[r - 1]] - b[q[r]]):
        r -= 1
    r += 1
    q[r] = i
print(f[n])
