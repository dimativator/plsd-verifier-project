mat = []

for x in range(0, 5):
    a = list(map(int, input().split()))
    mat.append(a)
    for i in a:
        if i == 1:
            row = a.index(1)
            col = mat.index(a)

print(abs(row - 2) + abs(col - 2))