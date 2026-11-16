t = int(input())
for _ in range(t):
	n,m = map(int,input().split())
	l = []
	s = 0
	t1,t2 = 0,0
	for i in range(n):
		l1 = list(map(int,input().split()))
		l.append(l1)
	for i in range(n):
		f = 1
		for j in range(m):
			if l[i][j] == 1:
				f = 0 
		if f:
			t1 += 1
	for i in range(m):
		f = 1
		for j in range(n):
			if l[j][i] == 1:
				f = 0
		if f:
			t2 += 1
	if min(t1,t2)%2 == 0:
		print("Vivek")
	else:
		print("Ashish")