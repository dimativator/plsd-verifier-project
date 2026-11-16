n, p, q = map(int, input().split())
s = input()
for i in range(n // p + 1):
    for j in range(n // q + 1):
        if i * p + j * q == n:
            print(i + j)
            for k in range(i):
                print(s[k * p: (k + 1) * p])
            for k in range(j):
                print(s[i * p + k * q: i * p + (k + 1) * q])
            exit()
print(-1)
