t=int(input())
for q in range(t):
	n=int(input())
	a=[list(map(int,input().split())) for i in range(n)]
	a.sort()
	ans=""
	x,y=0,0
	f=0
	for i in range(n):
		if a[i][0]>=x and a[i][1]>=y:
			ans+='R'*(a[i][0]-x)
			x=a[i][0]
			ans+='U'*(a[i][1]-y)
			y=a[i][1]
		else:
			f=1
			print('NO')
			break
	if f==0:
		print('YES')
		print(ans)
