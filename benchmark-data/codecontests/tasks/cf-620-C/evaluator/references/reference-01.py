n=int(input())
d={}
b=[]
e=1
a=list(map(int,input().split()))
for i in range(n):
	if a[i] in d:
		b.append([e,i+1])
		e=i+2
		d.clear()
	else:
		d[a[i]]=i+1	 
if len(b)==0:
	print(-1)
	exit()		
print(len(b))
k=b[-1]
b[-1]=[k[0],n]
for i in b:
	print(*i)		