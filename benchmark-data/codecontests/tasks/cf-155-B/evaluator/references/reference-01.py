n=int(input())
arr=[]
for i in range(n):
	a,b=map(int,input().split())
	arr.append((b,a))
arr.sort(reverse=True)
counter=1
ans=0
i=0
while(counter and i<n):
	counter-=1
	counter+=arr[i][0]
	ans+=arr[i][1]
	i+=1
print(ans)
