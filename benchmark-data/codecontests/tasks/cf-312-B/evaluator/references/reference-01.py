a, b, c, d = map(int, input().split(' '))
x = a/b
y = c/d
print(x / (1-(1-x) * (1-y)))
