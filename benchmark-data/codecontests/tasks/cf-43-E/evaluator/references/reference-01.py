import sys
from array import array  # noqa: F401


def input():
    return sys.stdin.buffer.readline().decode('utf-8')


n, s = map(int, input().split())
data = [dict() for _ in range(n)]

for i in range(n):
    k, *a = map(int, input().split())
    cur = 0
    for j in range(0, 2 * k, 2):
        data[i][cur] = a[j]
        cur += a[j + 1]

    data[i][cur] = 0


ans = 0

for i in range(n):
    for j in range(i + 1, n):
        state1 = 0
        dist_i, dist_j = 0, 0
        speed_i, speed_j = 0, 0
        time = sorted(set(data[i].keys()) | set(data[j].keys()))
        for t1, t2 in zip(time, time[1:]):
            if t1 in data[i]:
                speed_i = data[i][t1]
            if t1 in data[j]:
                speed_j = data[j][t1]

            dist_i += (t2 - t1) * speed_i
            dist_j += (t2 - t1) * speed_j
            state2 = 0 if dist_i == dist_j else 1 if dist_i > dist_j else 2

            if state2 != 0:
                if state1 | state2 == 3:
                    ans += 1
                state1 = state2
            if dist_i == s or dist_j == s:
                break

print(ans)
