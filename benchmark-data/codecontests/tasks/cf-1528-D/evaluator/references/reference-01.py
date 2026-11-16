import sys
input = lambda: sys.stdin.readline().rstrip()

def dijkstra(n, E, i0=0):
    D = [1 << 30] * n
    D[i0] = 0
    Q = set([i for i in range(n)])
    while Q:
        d = 1 << 30
        for q in Q:
            if D[q] < d:
                i = q
                d = D[q]
        Q.remove(i)
        for j, w in enumerate(E[i]):
            jj = (j + d) % n
            if jj == i: continue
            nd = d + w
            if D[jj] > nd:
                D[jj] = nd
    # return D
    return " ".join(map(str, D))


N, M = map(int, input().split())
inf = 2 * 10 ** 9
X = [[inf] * N for _ in range(N)]
for _ in range(M):
    a, b, c = map(int, input().split())
    X[a][b] = c
Y = [[0] * N for _ in range(N)]
for i, Yi in enumerate(Y):
    Xi = X[i]
    for j in range(N):
        if j and mi < Xi[j] + N - 1:
            mi = min(mi + 1, Xi[j])
            Yi[j] = mi
            continue
        mi = inf
        for k in range(N):
            mi = min(mi, Xi[j-k] + k)
        Yi[j] = mi

Z = [dijkstra(N, Y, s) for s in range(N)]
print("\n".join(Z))

