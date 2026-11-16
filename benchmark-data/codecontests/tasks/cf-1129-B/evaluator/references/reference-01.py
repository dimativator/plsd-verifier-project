def compute():
    from sys import stdin
    [k] = list(map(int, stdin.readline().split()))
    
    MAXX = 1000000
    MAXN = 2000

    o = [-1]
    k += 1
    while k>0:
        k += 1
        if k > MAXX:
            tosub = MAXX
        else:
            tosub = k
        o.append(tosub)
        k -= tosub

    if (len(o) > MAXN):
        print(-1)
    else:
        print(len(o))
        print(*o)


if __name__ == "__main__":
    compute()
