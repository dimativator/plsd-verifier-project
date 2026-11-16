n = int(input())
a = [int(i) for i in input().split()]
m = [0,0]
for i in range(n):
    m[0] += a[i] // 2
    m[1] += a[i] // 2
    if a[i] % 2 != 0:
        m[i % 2] += 1
print(int(min(m[0], m[1])))
