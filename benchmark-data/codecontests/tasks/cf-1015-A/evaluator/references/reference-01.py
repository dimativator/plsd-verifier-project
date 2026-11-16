n, m = [int(x) for x in input().split()]
s = set(range(1, m+1))

for _ in range(n):
    a, b = [int(x) for x in input().split()]
    s -= set(range(a, b+1))

print(len(s))
print(*s)
