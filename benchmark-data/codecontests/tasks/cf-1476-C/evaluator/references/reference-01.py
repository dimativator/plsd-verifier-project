import math,sys,bisect,heapq,os
from collections import defaultdict,Counter,deque
from itertools import groupby,accumulate
from functools import lru_cache
#sys.setrecursionlimit(200000000)
int1 = lambda x: int(x) - 1
def input(): return sys.stdin.readline().rstrip('\r\n')
#input = iter(sys.stdin.buffer.read().decode().splitlines()).__next__
aj = lambda: list(map(int, input().split()))
def list3d(a, b, c, d): return [[[d] * c for j in range(b)] for i in range(a)]
#MOD = 1000000000 + 7
def Y(c):  print(["NO","YES"][c])
def y(c):  print(["no","yes"][c])
def Yy(c):  print(["No","Yes"][c])



def solve():
	for _ in range(int(input())):
		n, = aj()
		c = aj()
		a = aj()
		b = aj()
		ans = 0
		tot = c[-1]
		for i in range(n-1,0,-1):
			tot += 2
			if a[i] > b[i]:
				a[i],b[i] = b[i],a[i]
			ans = max(ans,tot + b[i] - a[i] - 1)
			if a[i] == b[i]:
				tot = c[i-1]
			else:
				tot += a[i]-1
				tot += c[i-1]-b[i]
			tot = max(tot,c[i-1])
		print(ans)







try:
	#os.system("online_judge.py")
	sys.stdin = open('input.txt', 'r') 
	sys.stdout = open('output.txt', 'w')
except:
	pass

solve()