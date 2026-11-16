n, a, b = list(map(int, input().split()))

if b == 0:
	print(a)
	exit()

dx = b // abs(b)
for i in range(abs(b)):
	a += dx
	if a == 0:
		a = n
	elif a == n + 1:
		a = 1
print(a)