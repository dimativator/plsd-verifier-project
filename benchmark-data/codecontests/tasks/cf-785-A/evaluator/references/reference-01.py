a = int(input())
sum = 0
for i in range(1,a+1):
    b = input()
    if b == 'Tetrahedron':
        sum += 4
    elif b == 'Cube':
        sum += 6
    elif b == 'Octahedron':
        sum += 8
    elif b == 'Dodecahedron':
        sum += 12
    else:
        sum += 20
print(sum)