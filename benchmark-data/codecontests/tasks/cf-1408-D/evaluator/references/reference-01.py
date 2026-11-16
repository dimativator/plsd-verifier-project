n, m = map(int, input().split())

robbers = []
lights = []

for i in range(n):
    a, b = map(int, input().split())
    robbers.append((a, b))

for i in range(m):
    c, d = map(int, input().split())
    lights.append((c, d))

C = [0] * 1000002

for a, b in robbers:
    for c, d in lights:
        if a <= c:
            C[c - a] = max(C[c - a], d - b + 1)

result = 1000001
max_value = 0

for i in range(1000001, -1, -1):
    max_value = max(max_value, C[i])
    result = min(result, i + max_value)

print(result)