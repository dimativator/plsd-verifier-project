

A = [int(x) for x in input().split()]

N = 14

result = 0

for i in range(N):
    B = A[:]
    to_distribute = B[i]
    B[i] = 0
    for j in range(N):
        B[j] += to_distribute // N

    for j in range(1, to_distribute % N + 1):
        B[(i + j) % N] += 1

    result = max(result,
            sum([x for x in B if x % 2 == 0]))

print(result)
