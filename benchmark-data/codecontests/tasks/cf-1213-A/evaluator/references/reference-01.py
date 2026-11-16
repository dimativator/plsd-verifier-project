n = int(input())
v = list(map(int, input().split()))

a = []
b = []
for x in v:
  a.append(x) if x & 1 else b.append(x)

print(min(len(a), len(b)))

