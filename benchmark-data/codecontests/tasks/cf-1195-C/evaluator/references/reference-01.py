n=int(input())
a=[int(x) for x in input().split()]
b=[int(x) for x in input().split()]
dp=[[-1,-1] for i in range(n-1)]
dp.append([a[n-1],b[n-1]])
dp.append([0,0])
for i in range(n-1):
    dp[n-2-i][0]=a[n-2-i]+max(dp[n-1-i][1],dp[n-i][1])
    dp[n-2-i][1]=b[n-2-i]+max(dp[n-1-i][0],dp[n-i][0])
print(max(dp[0][0],dp[0][1]))
