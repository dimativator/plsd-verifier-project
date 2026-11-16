import sys
import math
from collections import defaultdict,Counter,deque
# input=sys.stdin.readline
# def print(x):
#     sys.stdout.write(str(x)+"\n")

import os
import sys
from io import BytesIO, IOBase

BUFSIZE = 8192


class FastIO(IOBase):
	newlines = 0

	def __init__(self, file):
		self._fd = file.fileno()
		self.buffer = BytesIO()
		self.writable = "x" in file.mode or "r" not in file.mode
		self.write = self.buffer.write if self.writable else None

	def read(self):
		while True:
			b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
			if not b:
				break
			ptr = self.buffer.tell()
			self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
		self.newlines = 0
		return self.buffer.read()

	def readline(self):
		while self.newlines == 0:
			b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
			self.newlines = b.count(b"\n") + (not b)
			ptr = self.buffer.tell()
			self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
		self.newlines -= 1
		return self.buffer.readline()

	def flush(self):
		if self.writable:
			os.write(self._fd, self.buffer.getvalue())
			self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
	def __init__(self, file):
		self.buffer = FastIO(file)
		self.flush = self.buffer.flush
		self.writable = self.buffer.writable
		self.write = lambda s: self.buffer.write(s.encode("ascii"))
		self.read = lambda: self.buffer.read().decode("ascii")
		self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# sys.stdout=open("CP2/output.txt",'w')
# sys.stdin=open("CP2/input.txt",'r')

def find(ind):
	ma=a[ind-1]
	end=0
	cur=n+1
	for j in range(k):
		if l1[j][2]>ma:
			if end<l1[j][1]:
				cur+=(l1[j][1]-end)*2
				end=l1[j][1]
				if cur>t:
					return 0
		end=max(end,l1[j+1][0]-1)
	return 1
# mod=pow(10,9)+7
# t=int(input())
for i in range(1):
	m,n,k,t=map(int,input().split())
	a=list(map(int,input().split()))
	a.sort(reverse=True)
	l1=[]
	for j in range(k):
		l,r,d=map(int,input().split())
		l1.append([l,r,d])
	l1.sort()
	l1.append([10**8,0,0])
	# print(l1)
	l=1
	r=m
	while l<=r:
		mid=(l+r)//2
		if find(mid):
			l=mid+1
		else:
			r=mid-1
		# print(l,r)
	print(r)
