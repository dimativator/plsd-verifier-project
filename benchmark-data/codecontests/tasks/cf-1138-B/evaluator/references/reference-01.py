import sys
import random

N = int(input())
C = list(map(int, input()))
A = list(map(int, input()))

# N = random.randint(20, 40) * 2
# C = [random.randint(0, 1) for i in range(N)]
# A = [random.randint(0, 1) for i in range(N)]

def build_solution(i, j, x, y):
	I = (0, 0)
	J = (0, 1)
	X = (1, 0)
	Y = (1, 1)
	ans = []
	for q in range(N):
		p = (C[q], A[q])
		if i and p == I:
			i -= 1
			ans.append(q+1)
		elif j and p == J:
			j -= 1
			ans.append(q+1)
		elif x and p == X:
			x -= 1
			ans.append(q+1)
		elif y and p == Y:
			y -= 1
			ans.append(q+1)
	return map(str, ans)

a = b = c = d = 0
for i in range(N):
	if C[i] == 0:
		if A[i] == 0:
			a += 1
		else:
			b += 1
	else:
		if A[i] == 0:
			c += 1
		else:
			d += 1
# print(C)
# print(A)
# print(a, b, c, d, "N/2=", N//2)


for i in range(0, a+1):
	y = - N//2 + i + b + d
	if y < 0:
		continue
	min_j = max(0, N//2 - i - c - y)
	max_j = min(b + 1, N //2 + 1)
	# print(i, y, '[', min_j, max_j, ']')
	for j in range(min_j, max_j):
		x = N//2 - i - j - y
		if x < 0:
			break
		# print("Check ", i, j, 'x, y:', x,  y)
		if not ((0 <= x <= c) and (0 <= y <= d)):
			continue

		# print('SOL', i, j, x, y)
		sol = build_solution(i, j, x, y)
		print(' '.join(sol))
		exit(0)

print(-1)


# 1) loop over N
# 2) pick best actor on every iteration
# 3) try to minimize diff between teams
# if len(first) == len(second) and first.score == second.score:
# 	print(' '.join(map(lambda x: str(x+1), first)))
# else:
# 	print(-1)





# a, b, c, d = 13 5 2 1, N = 20



# i, j, x, y, SUM = 10

# i = 0
# j = 0







