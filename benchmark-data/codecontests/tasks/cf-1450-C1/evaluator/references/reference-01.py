
def disti(b,ind):

	a=[]
	for i in b:
		h=[]
		for j in i: h.append(j)
		a.append(h)
	ans=0

	id=0

	for i in range(n):
		start = ind[id%3]
		id+=1
		for j in range(start ,n,3):

			left=''
			right=''
			up=''
			down=''
			mid1=''
			mid2=''

			if(j-2 >= 0): left = a[i][j-2] + a[i][j-1] + a[i][j]
			if(j+2 <n ): right = a[i][j+2] + a[i][j+1] + a[i][j]
			if(i+2 <n ): down = a[i+2][j] + a[i+1][j] + a[i][j]
			if(i-2 >= 0 ): up = a[i-2][j] + a[i-1][j] + a[i][j]
			if(i+1<n and i-1>=0) : mid1 = a[i-1][j] + a[i][j] + a[i+1][j]
			if(j+1<n and j-1>=0) : mid2 = a[i][j-1] + a[i][j] + a[i][j+1]

			

			ok=False
			for k in (left,right,up,down,mid1,mid2):
				if(k=='XXX' or k=='OOO'): ok=True

			# ok=True

			if(ok and a[i][j] == 'X') : 
				a[i][j] = 'O'
				ans+=1
			# elif(ok and a[i][j] == 'O') : a[i][j] = 'X'
	return a,ans

def P(b):
	for i in b: print(*i,sep="")

for _ in range(int(input())):

	n=int(input())
	a=[]
	tot=0
	for i in range(n):
		s=list(input())
		a.append(s)
		tot+= (n-s.count('.'))

	
	b1,s1 = disti(a,[1,0,2])
	b2,s2 = disti(a,[2,1,0])
	b3,s3 = disti(a,[0,2,1])
	
	if(s1*3 <=tot) : P(b1)
	elif(s2*3 <=tot) : P(b2)
	elif(s3*3 <=tot) : P(b3)
	# print(s1,s2,s3)
