def ncr(n, r, p):
    # initialize numerator
    # and denominator
    num = den = 1
    for i in range(r):
        num = (num * (n - i)) % p
        den = (den * (i + 1)) % p
    return (num * pow(den,
            p - 2, p)) % p


n = int(input())
a = sorted(list(map(int, input().split())))
ans = 0
for i in range(n):
    ans += abs(a[i] - a[2*n-1-i])
fac = ncr(2*n, n, 998244353)
print((fac * ans) % 998244353)
