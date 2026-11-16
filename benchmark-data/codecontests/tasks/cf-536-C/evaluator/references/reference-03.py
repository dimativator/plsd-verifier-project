from itertools import imap
import sys
n = input()


def parseints(s, n):
    r, i, x = [0] * n, 0, 0
    for c in imap(ord, s):
        if c == 32:
            r[i], i, x = x, i + 1, 0
        else:
            x = x * 10 + c - 48
    return r

z = parseints(sys.stdin.read().replace('\n', ' '), n * 2)
# p = zip(z[::2], z[1::2], range(1, n))
p = zip(z[::2], z[1::2])


def convex_hull(points):
    # points = list(set(points))
    # points.sort(reverse=True)

    if len(points) <= 1:
        return points

    pindex = range(len(points))
    pkey = [x * 10001 + y for x, y in points]
    pindex.sort(key=lambda i: pkey[i], reverse=True)


    def cross(o, a, b):
        ax, ay = a
        bx, by = b
        ox, oy = o
        return (oy * (ox * (ay * bx - ax * by) +
                      ax * bx * (by - ay)) -
                ox * ay * by * (bx - ax))
    # def cross(o, a, b):
    #     return (o[1] * (o[0] * (a[1] * b[0] - a[0] * b[1]) +
    #                     a[0] * b[0] * (b[1] - a[1])) -
    #             o[0] * a[1] * b[1] * (b[0] - a[0]))

    lower = []
    for pi in pindex:
        p = points[pi]
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) < 0:
            lower.pop()
        if not lower or lower[-1][1] < p[1]:
            lower.append(p)

    return lower

pdic = {}
for i, x in enumerate(p, 1):
    pdic.setdefault(x, []).append(i)

ch = convex_hull(p)
res = []
for x in ch:
    res.extend(pdic[x])

res.sort()
print ' '.join(map(str, res))
