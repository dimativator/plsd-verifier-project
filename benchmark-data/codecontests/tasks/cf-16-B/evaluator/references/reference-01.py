"""
read: 1:01
think: 2:46
code: 10:48
debug: --:--
status: TL
"""
n, m = map(int, input().split())

c = [list(map(int, input().split())) for i in range(m)]
c.sort(key=lambda x: x[1], reverse=True)

mx = 0
i = 0
while n > 0 and i < m:
    add = min(n, c[i][0])
    mx += add * c[i][1]
    n -= add
    i += 1


print(mx)