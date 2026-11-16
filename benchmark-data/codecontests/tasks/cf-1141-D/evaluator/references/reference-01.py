#Bhargey Mehta (Sophomore)
#DA-IICT, Gandhinagar
import sys, math, queue
sys.setrecursionlimit(1000000)
#sys.stdin = open("input.txt", "r")

n = int(input())
l = list(input())
r = list(input())
ls = {chr(i):[] for i in range(97, 97+26)}
rs = {chr(i):[] for i in range(97, 97+26)}
lc = []
rc = []
for i in range(n):
	if l[i] == "?": lc.append(i)
	else: ls[l[i]].append(i)
	if r[i] == "?": rc.append(i)
	else: rs[r[i]].append(i)
	
for k in ls:
	if len(ls[k]) > len(rs[k]):
		while len(rc) != 0 and len(ls[k]) != len(rs[k]):
			rs[k].append(rc[-1])
			rc.pop()
	elif len(ls[k]) < len(rs[k]):
		while len(lc) != 0 and len(rs[k]) != len(ls[k]):
			ls[k].append(lc[-1])
			lc.pop()

pairs = []
for k in ls:
	for i in range(min(len(rs[k]), len(ls[k]))):
		pairs.append((ls[k][i]+1, rs[k][i]+1))
for i in range(min(len(rc), len(lc))):
	pairs.append((lc[i]+1, rc[i]+1))

print(len(pairs))
for pair in pairs:
	print(*pair)
