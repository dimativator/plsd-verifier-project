#codeforces 42d: strange town: math, constructive algorithm

def readGen(trans):
	while 1:
		for x in input().split():
			yield(trans(x))
readint=readGen(int)

n=next(readint)

def constructRow(n):
	can=[1 for i in range(1001)]
	b=[0 for i in range(n+1)]
	b[2]=1
	b[3]=2
	can[1]=0
	can[2]=0
	for k in range(4,n+1):
		b[k]=b[k-1]+1
		while (not can[b[k]]): b[k]+=1
		can[b[k]]=0
		for i in range(2,k):
			for p in range(2,k):
				can[b[k]+b[p]-b[i]]=0
	return b

def constructMatrix(b,n):
	can=[1 for i in range(1001)]
	for i in range(2,n+1):
		for j in range(2,n+1):
			for p in range(2,n+1):
				can[b[2]+b[3]+b[p]-b[i]-b[j]]=0
	x=1
	while (not can[x]): x+=1
	a=[[0 for j in range(n+1)] for i in range(n+1)]
	for i in range(n+1):
		a[1][i]=a[i][1]=b[i]
	for i in range(2,n+1):
		for j in range(i+1,n+1):
			a[i][j]=a[j][i]=b[i]+b[j]+x-b[2]-b[3]
	return a
	
b=constructRow(n)
#print(b)

a=constructMatrix(b,n)
for i in range(1,n+1):
	for j in range(1,n+1):
		print("{:4}".format(a[i][j]),end='')
	print()
