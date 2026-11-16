s = input()

to_ans = [False for _ in range(len(s))]
def solve(s, left, right): #right inclusive
	if left >= right:
		return
	while left <= right and s[left] == ")":
		left += 1
	while right >= left and s[right] == "(":
		right -= 1
	if left >= right:
		return
	else:
		to_ans[left] = True
		to_ans[right] = True
		solve(s, left+1, right-1)

solve(s, 0, len(s)-1)

if sum(to_ans) == 0:
	print(0)
else:
	print(1)
	print(sum(to_ans))
	print(" ".join([str(item + 1) for item in range(len(s)) if to_ans[item]]))
