for I in range(int(input())):
    n,t = map(int,input().split())
    a = list(map(int,input().split()))
    d = []
    if t % 2 != 0:
        for i in range(n):
            if a[i] <= t // 2:
                d.append(1)
            else:
                d.append(0)
    else:
        p = 0
        for i in range(n):
            if a[i] < t//2:
                d.append(1)
            elif a[i] > t//2:
                d.append(0)
            else:
                d.append(p)
                p = (p + 1) % 2
    print(*d)