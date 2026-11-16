for _ in range(int(input())):
	n=int(input())
	l=list(map(int,input().split()))
	if len(set(l))==1:
		print(-1)
	else:
		m=max(l)
		for i in range(n):
			if i>0:
				if i<n-1:
					if l[i]==m and (l[i-1]<m or l[i+1]<m):
						print(i+1)
						break
				else:
					if l[i]==m and l[i-1]<m:
						print(i+1)
						break
			else:
				if l[i]==m and l[i+1]<m:
					print(i+1)
					break