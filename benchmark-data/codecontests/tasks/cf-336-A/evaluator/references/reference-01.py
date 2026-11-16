x,y=map(int,input().split())

w = abs(x)+abs(y)

if x<0:
	if y<0:
		print(-w,0,0,-w)
	else:
		print(-w,0,0,w)
else:
	if y<0:
		print(0,-w,w,0)
	else:
		print(0,w,w,0)