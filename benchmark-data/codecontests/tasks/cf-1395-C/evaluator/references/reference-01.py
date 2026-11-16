from sys import stdin
input=lambda : stdin.readline().strip()
from math import ceil,sqrt,factorial,gcd
from collections import deque
n,m=map(int,input().split())
a=list(map(int,input().split()))
b=list(map(int,input().split()))
z=[]
ma=0
for i in a:
	x=float("infinity")
	for j in b:
		x=min(i&j,x)
	ma=max(x,ma)
for i in a:
	t=float("infinity")
	for j in b:
		if t==float("infinity") or ma|(i&j)<ma|t:
			t=i&j
	z.append(t)
x=z[0]
for i in z:
	x=x|i
print(x)