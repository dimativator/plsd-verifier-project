import itertools
import math

n = int(input())
a = [int(x) for x in input().split()]
amin = min(a)
b = list(filter(lambda x: x[1] == amin, enumerate(a)))
l = len(b)
k = max((b[(i+1) % l][0] - b[i][0] - 1)%n for i in range(l))
print(amin*n + k)


