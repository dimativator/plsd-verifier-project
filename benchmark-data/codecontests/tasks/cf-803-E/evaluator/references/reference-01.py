n, k = [int(i) for i in input().split()]
s = input()
dp = [[False] * 2010 for i in range(1001)]

dp[0][0] = True

for i in range(n):
    l = -k + 1
    r = k
    if i == n - 1:
        l -= 1
        r += 1
    for b in range(l, r):
        if s[i] == 'L':
            dp[i + 1][b] = dp[i][b + 1]
        elif s[i] == 'W':
            dp[i + 1][b] = dp[i][b - 1]
        elif s[i] == 'D':
            dp[i + 1][b] = dp[i][b]
        else:
            dp[i + 1][b] = dp[i][b + 1] or dp[i][b - 1] or dp[i][b]

ans = [0] * n
i = n
b = -1

if dp[i][k]:
    b = k
elif dp[i][-k]:
    b = -k

if b == -1:
    print("NO")
else:
    while i > 0:
        if (s[i - 1] == 'L' or s[i - 1] == '?') and dp[i][b] == dp[i - 1][b + 1]:
            ans[i - 1] = 'L'
            b += 1
        elif (s[i - 1] == 'W' or s[i - 1] == '?') and dp[i][b] == dp[i - 1][b - 1]:
            ans[i - 1] = 'W'
            b -= 1
        else:
            ans[i - 1] = 'D'
        i -= 1
    for j in ans:
        print(j, end='')
