t = int(input())

for w in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    p = 0 if a[0] == 0 else 1
    a = a[1:]
    n1 = 0
    for x in a:
        if x == 0:
            n1 = 0
        else:
            n1 += 1
            if n1 % 3 == 0:
                p += 1

    print(p)
