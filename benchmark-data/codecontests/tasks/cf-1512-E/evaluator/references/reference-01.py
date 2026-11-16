t = int(input())
for _ in range(t):
    n, l, r, s = map(int, input().split())
    l -= 1
    r -= 1
    c = r - l + 1
    if c * (c + 1) // 2 > s or c * (2 * n + 1 - c) // 2 < s:
        print(-1)
        continue
    sec = [i for i in range(1, c + 1)]
    sec.reverse()
    s -= c * (c + 1) // 2
    cnt = 0
    while s > 0:
        s -= 1
        sec[cnt] += 1
        cnt = (cnt + 1) % c
    used = [False] * n
    ans = [0] * n
    ans[l:r+1] = sec
    for i in sec:
        used[i - 1] = True
    iter = 0
    for i in range(n):
        if ans[i]:
            continue
        while used[iter]:
            iter += 1
        used[iter] = True
        ans[i] = iter + 1
    print(*ans)
