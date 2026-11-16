n=int(input())
a1=[]
a2=[]
for i in range(n):
	x,d=list(map(int,input().split()))
	a1.append(x)
	a2.append(d)

flag=1
for i in range(n):
	for j in range(i+1,n):
		if ((a1[i]+a2[i]==a1[j]) and (a1[j]+a2[j]==a1[i])):
			print("YES")
			flag=0
			break
	if(flag==0):
		break
if(flag==1):
	print("NO")
