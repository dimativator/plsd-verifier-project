c = 0

for _ in range(int(input())):
    n = [int(x) for x in input().split()]
    n,m = n[0],n[1]

    if m - n >= 2:
        c += 1
print(c)
