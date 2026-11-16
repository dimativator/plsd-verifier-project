import sys
def fastio():
    from io import StringIO
    from atexit import register
    global input
    sys.stdin = StringIO(sys.stdin.read())
    input = lambda : sys.stdin.readline().rstrip('\r\n')
    sys.stdout = StringIO()
    register(lambda : sys.__stdout__.write(sys.stdout.getvalue()))
fastio()

def debug(*var, sep = ' ', end = '\n'):
    print(*var, file=sys.stderr, end = end, sep = sep)

INF = 10**20
MOD = 10**9 + 7
I = lambda:list(map(int,input().split()))
from math import gcd
from math import ceil
from collections import defaultdict as dd, Counter
from bisect import bisect_left as bl, bisect_right as br

n, w = I()
cups = I()
cups.sort()

def check(mid):
    girls = boys = 0
    ok = True
    ok &= cups[0] >= mid
    ok &= cups[n] >= 2 * mid
    return ok

lo, hi = 0, INF
count = 0
while hi - lo > 10 ** (-6):
    count += 1
    if count == 10000:
        break
    mid = (lo + hi) / 2
    if check(mid):
        lo = mid
    else:
        hi = mid - 1e-7
print(min(lo, w / (3 * n)) * 3 * n)