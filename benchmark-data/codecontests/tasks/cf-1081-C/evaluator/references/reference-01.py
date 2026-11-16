from math import factorial

[n, m, k] = [int(i) for i in input().split()]
mod = 998244353

l = m*((m-1)**k)
L = factorial(n-1)//factorial(n-1-k)//factorial(k)


print((l*L)%mod)
