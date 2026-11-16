#https://codeforces.com/contest/59/problem/E
class Pathclass:
	def __init__(self,node_number,nextnode):
		self.number = node_number
		self.next = nextnode

import collections
lis = input().split()
n,m,k = int(lis[0]),int(lis[1]),int(lis[2])
adjlis = [collections.deque([]) for i in range(n)]
for i in range(m):
	lis = input().split()
	x,y = int(lis[0])-1,int(lis[1])-1
	adjlis[x].append(y)
	adjlis[y].append(x)
triplet = [[] for i in range(n)]
for i in range(k):
	lis = input().split()
	a,b,c = int(lis[0])-1,int(lis[1])-1,int(lis[2])-1
	triplet[a].append((b,c))
node_queue = collections.deque([])
path_queue = collections.deque([])
flag = False
pp = Pathclass(0,None)
while  adjlis[0]:
	i = adjlis[0].popleft()
	if(i==n-1):
		flag = True
	node_queue.append(i)
	path_queue.append(Pathclass(i,pp))
if(flag):
	print(1)
	print(1,n)
else:
	finalpath = None
	while node_queue and not flag:
		node = node_queue.popleft()
		path = path_queue.popleft()
		lenn = len(adjlis[node])
		for j in range(lenn):
			i = adjlis[node].popleft()
			if (not (node,i) in triplet[path.next.number]):
				if(i==n-1):
					flag = True
					finalpath = Pathclass(i,path)
					break
				else:
					path2 = Pathclass(i,path)
					node_queue.append(i)
					path_queue.append(path2)
			else:
				adjlis[node].append(i)
	if not flag:
		print(-1)
	else:
		pathlist = []
		while finalpath:
			pathlist.append(finalpath.number + 1)
			finalpath = finalpath.next
		pathlist.reverse()
		print(len(pathlist)-1)
		for i in pathlist:
			print(i,end=" ")
		print()