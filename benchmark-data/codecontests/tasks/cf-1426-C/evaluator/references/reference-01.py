from math import ceil
for _ in range(int(input())):
    n = int(input())
    b = ceil(pow(n, 0.5))
    a = ceil(n / b)
    ans = a + b - 2
    print(ans)