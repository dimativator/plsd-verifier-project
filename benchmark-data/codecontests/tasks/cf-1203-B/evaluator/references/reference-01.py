q = int(input())
for w in range(q):
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    n *= 4
    x = a[0] * a[n - 1]
    ok = 1
    for i in range(0, n // 2, 2):
        if a[i] * a[n - i - 1] != x or a[i] != a[i + 1] or a[n - i - 1] != a[n - i - 2]:
            ok = 0
            break
    if ok:
        print('YES')
    else:
        print('NO')
    