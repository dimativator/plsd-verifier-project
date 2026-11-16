#: Author - Soumya Saurav
import sys,io,os,time
from collections import defaultdict
from collections import Counter
from collections import deque
from itertools import combinations
from itertools import permutations
import bisect,math,heapq
alphabet = "abcdefghijklmnopqrstuvwxyz"

input = sys.stdin.readline

########################################

alice = "Alice"
bob = "Bob"
tie = "Tie"

for ii in range(int(input())):
	n = int(input())
	arr = list(map(int , input().split()))
	arr.sort(reverse = True)
	a = 0
	b = 0
	turn = 1 #1 is alice
	#print(arr)
	for i in range(n):
		if arr[i]%2:
			if not turn:
				b += arr[i]
		else:
			if turn:
				a += arr[i]
		turn = not turn
	if a > b:
		print(alice)
	if a < b:
		print(bob)
	if a == b:
		print(tie)
	









'''
# Wrap solution for more recursion depth
for dx,dy in [[1,0],[0,1],[-1,0],[0,-1]]:
#submit as python3
import collections,sys,threading
sys.setrecursionlimit(10**9)
threading.stack_size(10**8)



threading.Thread(target=solve).start()
'''
