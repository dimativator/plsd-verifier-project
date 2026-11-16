def zip_sorted(a,b):

	# sorted  by a
	a,b = zip(*sorted(zip(a,b)))
	# sorted by b
	sorted(zip(a, b), key=lambda x: x[1])

	return a,b

import sys
input = sys.stdin.readline
I = lambda : list(map(int,input().split()))
S = lambda : list(map(str,input()))


t,=I()
for t1 in range(t):
	a   = I()
	if sum(a)%9==0:
		if min(a)>=int(sum(a)/9):
			print('yes')
		else:
			print('no')
	else:
		print('no')
