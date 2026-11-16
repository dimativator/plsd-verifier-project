def powmod(x, k, m):
    res = 1
    s = 1
    while s <= k:
        if k & s:
            res = res * x % m
        x = x * x % m
        s <<= 1
    return res
m = 998244353
w, h = map(int, input().split())
print(powmod(2, w + h, m))
