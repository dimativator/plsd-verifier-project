from functools import reduce
from operator import xor

for _ in range(int(input())):
	n = int(input())
	a = [*map(int, input().split())]
	print(2)
	print(sum(a) + reduce(xor, a), reduce(xor, a))