q = int(input())
for i in range(q):
    k = 0
    c, m, x = [int(s) for s in input().split()]

    if min(c, m, x) != x:
        print(min(c, m))

    else:
        k += x
        z = (c + m - 2 * x) // 3
        print(k + min(z, c - x, m - x))
