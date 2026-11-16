import sys
input = sys.stdin.readline
import math

n, k = map(int, input().split())
B = sorted(map(int, input().split()), reverse=True)
N = 5 * (n + max(B))
A = [0] * N
A[0] = 1
A[1] = -1
ans = float("inf")
total = 0
j = 0
for i in range(N - 1):
    total += A[i]
    A[i + 1] += A[i]
    if total + A[i + 1] >= k:
        ans = min(ans, i + 1)
    while A[i] > 0 and j < n:
        u = (B[j] - 1) // 2
        v = B[j] - 1 - u
        A[i + 2] += 1
        A[i + 2 + u] -= 1
        A[i + 2] += 1
        A[i + 2 + v] -= 1
        A[i] -= 1
        total -= 1
        j += 1
print(ans if ans < float("inf") else -1)



