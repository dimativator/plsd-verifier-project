import sys,math
from collections import deque
#input = sys.stdin.buffer.readline


def solve():	
	return;


# for _ in range(int(input())):
# 	solve()


n = int(input())
h = input()

cnt=0
for i in range(n):
	s = input()
	if h==s[:3] or h==s[-3:]:
		cnt+=1

if cnt%2==0:
	print("home")
else:
	print("contest")

