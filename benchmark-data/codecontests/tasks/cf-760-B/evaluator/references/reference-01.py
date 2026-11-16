n, m, k = map(int, input().split())

m -= n
d = 0
k -= 1
out = 1
while m > 1 and d != max(k, n - k - 1):
    out += 1
    m -= 1
    left = min(d, k)
    right = min(d, n - k - 1)
    d += 1
    m -= left
    m -= right
out += m // n

print(out)
