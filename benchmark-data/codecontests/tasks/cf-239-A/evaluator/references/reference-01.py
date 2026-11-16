"""
    author - Sayan Bose
    Brooklyn 99 is love!
"""

y, k, n = map(int, input().split())
if n-y == 0:
	print(-1)
else:
	y1 = y
	res = []
	f, f1 = 0, 0
	while y <= n:
		if not y%k:
			f = 1
			if y-y1:
				f1 = 1
				print(y-y1, end = ' ')
		if not f:
			temp = y//k + 1
			y = k * temp
		else:
			y += k
	if not f1:
		print(-1)