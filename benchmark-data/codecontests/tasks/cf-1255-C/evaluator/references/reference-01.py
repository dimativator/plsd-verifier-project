def zip_sorted(a,b):

	# sorted  by a
	a,b = zip(*sorted(zip(a,b)))
	# sorted by b
	sorted(zip(a, b), key=lambda x: x[1])

	return a,b

def return_nxt(i,a,b):

	visited.add(i)

	c = (set(mem2[i])-set([a,b])).pop()

	final.append(c)



	if len(final)==n:

		return -1,b,c

	new_idx = ((set(mem1[b])-visited)&(set(mem1[c])-visited)).pop()

	return new_idx,b,c

import sys
input = sys.stdin.readline
I = lambda : list(map(int,input().split()))
S = lambda : list(map(str,input().split()))


from collections import  defaultdict
mem1 = defaultdict(list)
mem2 = defaultdict(list)
n,=I()

for t1 in range(n-2):
	a,b,c=I()
	mem2[t1] = [a,b,c]
	mem1[a].append(t1)
	mem1[b].append(t1)
	mem1[c].append(t1)
start1 = -1
start2 = -1
start_idx = -1
for i in mem1:
	if len(mem1[i])==1:
		start1 = i
		idx = mem1[i][0]
		start_idx = mem1[i][0]
		for j in range(len(mem2[idx])):
			val = mem2[idx][j]
			if len(mem1[val])==2:
				start2 = val
				break
		break
final = [start1,start2]
visited = set()
for i in range(n-2):
	start_idx,start1,start2 = return_nxt(start_idx,start1,start2)
print(*final)
