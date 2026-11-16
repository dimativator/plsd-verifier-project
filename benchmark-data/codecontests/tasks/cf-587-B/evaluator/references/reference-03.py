from collections import Counter
mod = 1000000007
n, l, k = map(int, raw_input().split())
a = map(int, raw_input().split())
b = []
count_a = Counter(a)
count_a_keys = sorted(count_a.keys())
rev_map = {}
for i, key in enumerate(count_a_keys):
    rev_map[key] = i
    b.append(count_a[key])

m = l / n
rest = l % n
dp = [[0 for j in range(len(b))] for i in range(k + 1)]
sum_dp = [[0 for j in range(len(b))] for i in range(k + 1)]

for i in range(len(b)):
    if len(dp) <= 1:
        break
    dp[1][i], sum_dp[1][i] = b[i], b[i]
    if i > 0:
        sum_dp[1][i] += sum_dp[1][i - 1]
for i in range(2, min(k + 1, m + 1)):
    for x in range(len(b)):
        dp[i][x] = b[x] * sum_dp[i - 1][x] % mod
        if x == 0:
            sum_dp[i][x] = dp[i][x] % mod
        else:
            sum_dp[i][x] = (dp[i][x] + sum_dp[i][x - 1]) % mod

ans = 0
for i in range(1, k + 1):
    ans = (ans + (m - i + 1) * sum_dp[i][len(b) - 1]) % mod

for j in range(rest):
    x = rev_map[a[j]]
    ans = (ans + 1) % mod
    for i in range(1, k):
        if i > m:
            continue
        ans = (ans + sum_dp[i][x]) % mod
print ans
