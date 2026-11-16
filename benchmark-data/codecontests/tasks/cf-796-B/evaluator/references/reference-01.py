n , m , k = list(map(int,input().split()))

h = list(map(int,input().split()))

used = [0] * int(1e7) 

for x in h:
	used[x] = 1 

t = 1

for i in range(k):
	u , v = list(map(int,input().split()))
	if used[t]:
		print(t) 
		exit(0)
	elif u == t:
		if used[v] == 1:
			print(v) 
			exit(0)
		t = v 
	elif v == t:
		if used[u] == 1:
			print(u) 
			exit(0)
		t = u 
print(t)
