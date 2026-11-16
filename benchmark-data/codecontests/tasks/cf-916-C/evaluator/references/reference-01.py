INF = 1000000
erast = [1] * INF
erast[1] = 0

primes = []
for i in range(2, INF):
    if erast[i] == 1:
        for j in range(i * 2, INF, i):
            erast[j] = 0
        primes.append(i)
# print(primes)
lastp = primes[-1]
n, m = map(int, input().split())
edges = set()
print(lastp, lastp)
for i in range(n - 2):
    print(i + 1, i + 2, 1)
    edges.add((i, i + 1))
    edges.add((i + 1, i))

print(n - 1, n, lastp - n + 2)
edges.add((n - 1, n))
edges.add((n, n - 1))

m -= n - 1
for i in range(0, n):
    for j in range(0, n):
        if i == j: continue
        if m == 0: break
        if not (i, j) in edges:
            m -= 1
            print(i + 1, j + 1, INF)
            edges.add((i, j))
            edges.add((j, i))


