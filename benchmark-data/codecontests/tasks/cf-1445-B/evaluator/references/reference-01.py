for k in range(int(input())):
    a, b, c, d = input().split()
    a, b, c, d = int(a), int(b), int(c), int(d)
    if a+b >= c+d:
        print(a+b)
    else:
        print(c + d)
