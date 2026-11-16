from sys import stdin, stdout
t=int(stdin.readline())
for _ in range(t):
	n=int(stdin.readline())
	arr=list(map(int,stdin.readline().split()))
	arr.sort()
	dp=[[10**9 for _ in range(2*n)] for _ in range(n)]

	for i in range(0,n):
		for j in range(1,2*n):
			if i==0:
				dp[i][j]=min(dp[i][j-1],abs(arr[i]-j))
			else:
				dp[i][j]=min(dp[i][j-1],dp[i-1][j-1]+abs(arr[i]-j))

	print(dp[n-1][2*n-1])