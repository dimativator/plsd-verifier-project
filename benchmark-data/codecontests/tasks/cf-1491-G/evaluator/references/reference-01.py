import sys
input = sys.stdin.readline

n = int(input());A = [0] + list(map(int, input().split()));seen = [0] * (n + 1);cycles = [];ans = []
for i in range(1, n + 1):
    cur = [];j = i
    while not seen[j]:cur.append(j);seen[j] = 1;j = A[j]
    if len(cur) > 1: cycles.append(cur)
def swap(x, y):A[x], A[y] = A[y], A[x];ans.append((x, y))
for i in range(1, len(cycles), 2):
    X, Y = cycles[i - 1], cycles[i];swap(X[0], Y[0])
    for x in X[1:]: swap(x, Y[0])
    for y in Y[1:]: swap(y, X[0])
    swap(X[0], Y[0])
if len(cycles) % 2:
    X = cycles[-1]
    if len(X) > 2:
        for x in X[:-2]: swap(x, X[-1])
        swap(X[0], X[-2]);swap(X[-2], X[-1]);swap(X[0], X[-1])
    else:
        Y = []
        for i in range(1, n + 1):
            if i != X[0] and i != X[1]: break
        swap(i, X[0]);swap(i, X[1]);swap(i, X[0])
print(len(ans))
for a in ans: print(*a)