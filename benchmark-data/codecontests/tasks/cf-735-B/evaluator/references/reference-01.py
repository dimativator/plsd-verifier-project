n, n1, n2 = [int(x) for x in input().split()]
d = [int(x) for x in input().split()]
d.sort(reverse=True)
s1 = 0
s2 = 0
n1, n2 = min(n1, n2), max(n1, n2)
for i in range(n1):
    s1 += d[i]
for i in range(n1, n1 + n2):
    s2 += d[i]
ans = s1 / n1 + s2 / n2
print(ans)