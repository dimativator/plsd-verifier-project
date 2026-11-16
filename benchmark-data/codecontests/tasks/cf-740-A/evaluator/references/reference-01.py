

n, a, b, c = map(int, input().split())
h=n%4
if h==0:
	d=0
else:
	if h==1:
		d=min(a*3,a+b,c)
	if h==2:
		d=min(a*2,b,c*2)
	if h==3:
		d=min(a,b+c,c*3)
print(d)