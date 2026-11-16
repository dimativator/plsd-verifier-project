n, x = map(int, input().split())
m = list(map(int, input().split()))
m.sort()
ans = 0
for i in range(n):
    ans += m[i] * x
    if x > 1:
        x -= 1
print(ans)
