def run1(unit,cst):
    cst *= unit
    for j in range(cnt+1)[::-1]:
        if dp[j] >= cst:
            dp[j+unit] = max(dp[j+unit],dp[j] - cst)


n,w,b,x = map(int,raw_input().split(" "))
cap = map(float,raw_input().split(" "))
cost = map(float,raw_input().split(" "))
dp = [-1.]*10005
dp[0] = float(w)
cnt = 0
w,b,x = float(w),float(b),float(x)
for i in range(n):
    unit = 1
    rest = cap[i]
    while unit <= rest:
        run1(int(unit),cost[i])
        cnt += unit
        rest -= unit
        unit *= 2
    if rest:
        run1(int(rest),cost[i])
        cnt += int(rest)
    for j in range(cnt+1)[::-1]:
        if dp[j]>=0:
            dp[j] = min(w+j*b,dp[j]+x)
ans = 0
for j in range(cnt+1):
    if dp[j] >=0:
        ans = j
print ans
