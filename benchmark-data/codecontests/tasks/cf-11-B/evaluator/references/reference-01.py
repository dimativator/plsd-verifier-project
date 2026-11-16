from math import sqrt
x = abs(int(input()))
n = int((sqrt(1 + 8 * x) - 1) / 2)
k = (n * (n + 1)) // 2
if k == x: print(n)
else:
    n += 1
    k += n
    if (k - x) % 2: 
        n += 1
        k += n
        print(n + (k - x) % 2)
    else: print(n)