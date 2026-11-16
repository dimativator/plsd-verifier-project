for _ in range(int(input())):
	n = int(input())
	a = list(map(int, input().split()))
	b = set(a)
	maxBall = 0
	for i in b:
		if a.count(i)>maxBall:
			maxBall=a.count(i)
	print(maxBall)