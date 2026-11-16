e = [[False] * 5 for i in range(5)]
for i in range(int(input())):
    a, b = map(int, input().split())
    e[a - 1][b - 1] = e[b - 1][a - 1] = True
for a in range(3):
    for b in range(a + 1, 4):
        for c in range(b + 1, 5):
            if len({e[a][b], e[a][c], e[b][c]}) == 1:
                print('WIN')
                exit()
print('FAIL')
