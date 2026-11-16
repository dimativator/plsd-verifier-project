import sys

def solve():
	n = int(input())
	if n%2 == 0:
		ans = "Mahmoud"
	else:
		ans = "Ehab"
	return ans
ans = solve()
print(ans)