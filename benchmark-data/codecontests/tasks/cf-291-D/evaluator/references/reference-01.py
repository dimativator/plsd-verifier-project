n, k = map(int, input().split())
a = [1 for i in range(n + 1)]
a[n] = 0
for iter in range(k):
    for i in range(1, n - 1):
        target = n - i
        if a[i + 1] > target - a[i]:
            # find right number
            target -= a[i]
            print(n - target, end=' ')
            a[i] += a[n - target];
        else:
            a[i] += a[i + 1]
            print(i + 1, end=' ')
    for i in range(max(0, n - 2), n):
        print(n, end=' ')
    print()
