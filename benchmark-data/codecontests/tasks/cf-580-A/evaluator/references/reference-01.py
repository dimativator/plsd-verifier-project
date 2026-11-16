n,a=int(input()),list(map(int,input().split()))
mx=1
c=1
for i in range(n-1):
	if(a[i+1]>=a[i]):
		c+=1
		if(c>mx):
			mx=c
	else:
		c=1
print(mx)