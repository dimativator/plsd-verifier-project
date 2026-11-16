from sys import stdin


def main():
    n, m, q = map(int, input().split())
    c = sz = 1 << n
    costs, cnt = [0] * sz, [0] * sz
    for w in map(int, input().split()):
        c //= 2
        for i in range(c, sz, c * 2):
            for j in range(i, i + c):
                costs[j] += w
    for i, c in enumerate(costs):
        if c > 101:
            costs[i] = 101
    costs.reverse()
    l = stdin.read().splitlines()
    for s in l[:m]:
        cnt[int(s, 2)] += 1
    del l[:m]
    cache = []
    for i in range(sz):
        row = [0] * 102
        cache.append(row)
        for j, c in enumerate(cnt):
            row[costs[i ^ j]] += c
        a = 0
        for j, b in enumerate(row):
            a += b
            row[j] = a
    for i, s in enumerate(l):
        row = s.split()
        l[i] = str(cache[int(row[0], 2)][int(row[1])])
    print('\n'.join(l))


if __name__ == '__main__':
    main()
