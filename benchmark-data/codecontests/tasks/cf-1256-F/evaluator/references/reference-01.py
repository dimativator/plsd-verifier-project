import sys, math
import io, os
#data = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
#from bisect import bisect_left as bl, bisect_right as br, insort
from heapq import heapify, heappush, heappop
from collections import defaultdict as dd, deque, Counter
#from itertools import permutations,combinations
def data(): return sys.stdin.readline().strip()
def mdata(): return list(map(int, data().split()))
def outl(var) : sys.stdout.write(' '.join(map(str, var))+'\n')
def out(var) : sys.stdout.write(str(var)+'\n')
#from decimal import Decimal
#from fractions import Fraction
#sys.setrecursionlimit(100000)
INF = float('inf')
mod = int(1e9)+7

def cal(s):
    l=[0]*26
    cnt=0
    for i in s:
        for j in range(ord(i)-97+1,26):
            cnt+=l[j]
        l[ord(i)-97]+=1
    return cnt

for q in range(int(data())):
    n=int(data())
    s=data()
    t=data()
    cnt_s=cal(s)
    cnt_t=cal(t)
    if (cnt_s==cnt_t or abs(cnt_s-cnt_t)%2==0 or max(Counter(s).values())>1) and (Counter(s)==Counter(t)):
        out("YES")
    else:
        out("NO")