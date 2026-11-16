import sys
import heapq
input = sys.stdin.readline
MOD = int(1e9+7)

n, x = list(map(int, input().split()))
a = list(map(int, input().split()))
s, h = sum(a), []
for i in a:
    heapq.heappush(h, s-i)
p, cnt = 0, 0
while h:
    z = heapq.heappop(h)
    if p == z:
        cnt += 1
        if cnt == x:
            heapq.heappush(h, p + 1)
            cnt = 0
    else:
        if cnt > 0:
            print(pow(x, min(p, s), MOD))
            exit()
        cnt = 1
        p = z
print(pow(x, min(p, s), MOD))
