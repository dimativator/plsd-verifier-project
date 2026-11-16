from sys import stdin, stdout
n = int(stdin.readline())
a = [int(i) for i in stdin.readline().split()]
d = dict()
ans, sm = 0, 0
for i in range(n):
    if a[i] not in d.keys():
        d[a[i]] = 0
    d[a[i]] += 1
    ans += i * a[i] - sm
    if (a[i] + 1) in d.keys():
        ans += 1 * d[a[i] + 1]
    if (a[i] - 1) in d.keys():
        ans -= 1 * d[a[i] - 1]
    sm += a[i]
stdout.write(str(ans))
