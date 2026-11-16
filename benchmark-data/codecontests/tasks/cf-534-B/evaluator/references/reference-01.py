from collections import Counter,defaultdict,deque
import heapq as hq
from itertools import count, islice

#alph = 'abcdefghijklmnopqrstuvwxyz'
#from math import factorial as fact
import math
import sys
input=sys.stdin.readline
#print=sys.stdout.write
#tt = int(input())
#total=0
#n = int(input())
#n,m,k = [int(x) for x in input().split()]
#n = int(input())
#l,r = [int(x) for x in input().split()]
v1,v2 = [int(x) for x in input().split()]
t,d = [int(x) for x in input().split()]
f = [v1]
b = [v2]
for i in range(t-1):
    f.append(f[-1]+d)
    b.append(b[-1]+d)
b.reverse()
ans = 0
for i in range(t):
    ans+=min(b[i],f[i])
print(ans)
