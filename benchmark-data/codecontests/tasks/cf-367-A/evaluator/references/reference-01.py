import sys


# sys.stdin = open('input.txt', 'r')
# sys.stdout = open('output.txt', 'w')

input = sys.stdin.readline


s = input().strip()
x_c, y_c, z_c = [0], [0], [0]

for el in s:
    x_c.append(x_c[-1]+int(el=="x"))
    y_c.append(y_c[-1]+int(el=="y"))
    z_c.append(z_c[-1]+int(el=="z"))

for _ in range(int(input())):
    l, r = map(int, input().split())
    if r - l < 2:
        print("YES")
        continue
    x, y, z = x_c[r]-x_c[l-1], y_c[r]-y_c[l-1], z_c[r]-z_c[l-1]
    if max(x, y, z) - min(x, y, z) > 1:
        print("NO")
    else:
        print("YES")