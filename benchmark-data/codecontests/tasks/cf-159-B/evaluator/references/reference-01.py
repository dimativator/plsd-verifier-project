def main():
    from sys import stdin
    l = list(map(int, stdin.read().split()))
    n, yx = l[0] * 2, [[0] * 1001 for _ in range(1001)]
    cnt = yx[0]
    u = v = 0
    for y, x in zip(l[3:n + 3:2], l[2:n + 2:2]):
        cnt[y] += 1
        yx[y][x] += 1
    ba, l = list(zip(l[n + 3::2], l[n + 2::2])), []
    for y, x in ba:
        if yx[y][x]:
            yx[y][x] -= 1
            cnt[y] -= 1
            v += 1
        else:
            l.append(y)
    for y in l:
        if cnt[y]:
            cnt[y] -= 1
            u += 1
    print(u + v, v)


if __name__ == '__main__':
    main()
