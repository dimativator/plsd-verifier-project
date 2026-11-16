def sum_digit(n):
	c=0
	x=n
	while x>0:
		c+=(x%10)
		x=x//10
	return c
n,m=map(int,input().split())
r='5'
su=5
while su<n:
	r='4'+r 
	su+=4
r=r[0:len(r)-1]
r+='5'
t1=""
for i in range(len(r)):
	t1+='5'
print(int(t1))
print(int(r))
