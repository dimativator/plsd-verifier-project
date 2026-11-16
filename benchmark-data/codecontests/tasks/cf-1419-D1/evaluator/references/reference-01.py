n = int(input())
a = sorted([int(i) for i in input().split()])

b = []
for i in range(n // 2):
    b.append(a[-1-i])
    b.append(a[i])
if n % 2 == 1:
    b.append(a[n // 2])

print((n - 1) // 2)
print(' '.join([str(i) for i in b]))
