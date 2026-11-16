import itertools as it

n = int(input())
res = None

for i in range(4):
    a = list(map(int, input().split()))
    for v in list(it.product(a[:2], a[2:])):
        if sum(v) <= n:
            res = [i + 1, v[0], n - v[0]]
            break
    if res is not None:
        break

print(-1 if res is None else ' '.join(map(str, res)))

