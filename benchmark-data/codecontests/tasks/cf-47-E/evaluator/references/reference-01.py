import sys
from array import array  # noqa: F401
from math import pi, sin, cos
from bisect import bisect_left


def input():
    return sys.stdin.buffer.readline().decode('utf-8')


n, v = map(int, input().split())
v = float(v)
alpha = [float(input()) for _ in range(n)]
m = int(input())
wall = sorted(tuple(map(float, input().split())) for _ in range(m)) + [(1e9, 1e9)]
max_angle = pi / 4
eps = 1e-9
a = [0.0] * m + [max_angle + eps]

for i in range(m):
    ng_angle, ok_angle = 0.0, max_angle + eps

    for _ in range(50):
        mid_angle = (ok_angle + ng_angle) / 2
        t = wall[i][0] / (v * cos(mid_angle))
        if (v * sin(mid_angle) * t - 9.8 * t**2 / 2) - eps <= wall[i][1]:
            ng_angle = mid_angle
        else:
            ok_angle = mid_angle

    a[i] = max(a[i], ng_angle)
    a[i + 1] = max(a[i], a[i + 1])


ans = [''] * n
for i in range(n):
    wi = bisect_left(a, alpha[i])

    ok, ng = 0.0, 1e7
    sin_a = sin(alpha[i])

    for _ in range(50):
        t = (ok + ng) / 2
        if v * sin_a * t - 9.8 * t**2 / 2 >= 0.0:
            ok = t
        else:
            ng = t

    x = v * cos(alpha[i]) * ok

    if x < wall[wi][0]:
        ans[i] = f'{x:.8f} {0:.8f}'
    else:
        ok, ng = 0.0, 1e7
        cos_a = cos(alpha[i])

        for _ in range(50):
            t = (ok + ng) / 2
            if v * cos_a * t <= wall[wi][0]:
                ok = t
            else:
                ng = t
        y = v * sin_a * ok - 9.8 * ok**2 / 2
        ans[i] = f'{wall[wi][0]:.8f} {y:.8f}'

print('\n'.join(ans))
