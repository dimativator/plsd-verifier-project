import sys

T = int(sys.stdin.readline().strip())
for t in range (0, T):
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    ans = 0
    for i in range (1, n):
        if a[i] < a[i-1]:
            ans = ans + a[i-1] - a[i]
    print(ans)