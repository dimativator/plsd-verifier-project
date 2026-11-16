f = [0] * 22
f[0], f[1], idx = [int(x) for x in input().split()]
for i in range (2, 22) : f[i] = f[i - 1] + f[i - 2]
print(f[idx])