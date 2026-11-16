from math import factorial

def c(n, k):
    cur = factorial(n) // factorial(k)
    return cur // factorial(n - k)

n = int(input())
ans = c(n, 5) + c(n, 6) + c(n, 7)

print(ans)

