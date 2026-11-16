from sys import *
input = stdin.readline

def solve(n, a, t):
	ans = 0
	for i in range(n):
		sum = 0
		high1 = a[i].bit_length()-1
		for j in range(i+1, n-1):
			high2 = a[j+1].bit_length()-1
			sum += a[j]
			if(sum >= (1<<(high1+1))):
				break
			if((a[i]^a[j+1]) == sum and (t == 0 or high1 != high2)):
				ans += 1
	return ans


n = int(input())
a = list(map(int, input().split()))
ans = solve(n, a, 0)
a = a[::-1]
ans += solve(n, a, 1)
print(ans)