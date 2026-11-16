import math
n1,n2  = map(int ,input().split())
a,b,d = 0,0,0
for i in range(1,7):
	d1 = abs(i-n1)
	d2 = abs(i-n2)
	if d1<d2:
		a+=1
	elif d1>d2:
		b+=1
	else:
		d+=1
print(a,d,b)
