n, s, g, c, r = int(input()), input(), 'ACGT', [], '==='
if n % 4 != 0:
    exit(print(r))
for i in g:
    c.append(s.count(i))
    if c[-1] > n // 4:
        exit(print(r))
for i in range(4):
    for j in range(c[i], n // 4):
        s = s.replace('?', g[i], 1)
print(s)
