n, m = list(map(int, input().split()))
a = list(map(int, input().split()))
t = 0
for i in range(m):
    cnt = a.count(i + 1)
    t += cnt * (n - cnt)
    n -= cnt
print(t)
