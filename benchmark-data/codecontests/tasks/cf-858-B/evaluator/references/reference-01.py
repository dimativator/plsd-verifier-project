n, m = map(int, input().split())
a = [tuple(map(int, input().split())) for i in range(m)]
ans = set()
for i in range(1, 101):
    can = True
    for k, f in a:
        if (k + i - 1) // i != f:
            can = False
            break
    if can:
        ans.add((n + i - 1) // i)
if len(ans) == 1:
    print(ans.pop())
else:
    print('-1')
