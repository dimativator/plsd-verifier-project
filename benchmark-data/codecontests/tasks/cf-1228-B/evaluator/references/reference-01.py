n, m = map(int, input().split())
row = list(map(int, input().split()))
col = list(map(int, input().split()))
grid = [['?'] * m for _ in range(n)]
for i in range(n):
    lng = row[i]
    for j in range(lng):
        grid[i][j] = 'b'
    if lng < m:
        grid[i][lng] = 'w'
for i in range(m):
    lng = col[i]
    for j in range(lng):
        if grid[j][i] != 'w':
            grid[j][i] = 'b'
        else:
            print(0)
            exit(0)
    if lng < n:
        if grid[lng][i] != 'b':
            grid[lng][i] = 'w'
        else:
            print(0)
            exit(0)
comb = 1
for _ in range(sum(map(lambda l: l.count('?'), grid))):
    comb = (comb * 2) % 1000000007
print(comb)
