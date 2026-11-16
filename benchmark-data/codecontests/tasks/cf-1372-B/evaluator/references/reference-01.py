from math import ceil, sqrt

for _ in range(int(input())):
    n = int(input())
    if n % 2 == 0: print(n // 2, n // 2)
    else:
        for i in range(3, ceil(sqrt(n)) + 1):
            if n % i == 0:
                print(n // i, n - (n // i))
                break
        else:
            print(1, n - 1)
