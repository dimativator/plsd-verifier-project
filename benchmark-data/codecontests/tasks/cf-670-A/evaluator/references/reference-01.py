n = int(input())

if n % 7 == 0:
    print(n // 7 * 2, n // 7 * 2)
else:
    x = (n // 7 + 1) * 7
    if x - n == 6:
        print((n // 7) * 2, (n // 7) * 2 + 1)
    else:
        if x - n == 1:
            print((n // 7) * 2 + 1, (n // 7) * 2 + 2)
        else:
            print((n // 7) * 2, (n // 7) * 2 + 2)
