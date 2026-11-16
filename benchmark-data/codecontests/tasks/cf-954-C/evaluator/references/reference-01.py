def main():
    int(input())
    a = list(map(int, input().split()))

    ds = [i - j for i, j in zip(a[1:], a)]
    dss = set(abs(x) for x in ds)
    if 0 in dss:
        return False
    try:
        dss.remove(1)
    except KeyError:
        pass
    if len(dss) > 1:
        return False
    if not dss:
        return 1e9, 1e9

    y = next(iter(dss))
    for d, c in zip(ds, a):
        j = (c - 1) % y
        if d == 1 and j == y - 1:
            return False
        if d == -1 and j == 0:
            return False
    return 1e9, y


ans = main()
if ans:
    print('YES')
    print('%d %d' % ans)
else:
    print('NO')
