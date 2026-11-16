def gcd(x,y):
    while x % y > 0:
        x, y = y, x % y
    return y
n = int(input())
a, b, c = [int(x) for x in input().split()], [int(x) for x in input().split()], [{} for i in range(n)]
def f(i,g):
    if g == 1:
        return 0
    if i == n:
        return 100000000000
    if g in c[i]:
        return c[i][g]
    A = f(i+1,g)
    A = min(A, f(i+1, gcd(g,a[i])) + b[i])
    c[i][g] = A
    return A
if f(0,0) < 100000000000:
    print(f(0,0))
else:
    print(-1)