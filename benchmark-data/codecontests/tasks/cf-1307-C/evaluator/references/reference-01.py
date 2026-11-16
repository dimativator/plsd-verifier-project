import os
import sys
def main():
	s=input()
	dp=[[0]*(27) for i in range(27)]
	d=[0]*27
	for i in range(len(s)):
		k=ord(s[i])-97
		for j in range(27):
			dp[k][j]+=d[j]
		d[k]+=1
	ans=0
	for i in range(27):
		for j in range(27):
			ans=max(ans, dp[i][j])
	for i in d:
		ans=max(ans , i)
	print(ans)
if __name__ == "__main__":
    main()