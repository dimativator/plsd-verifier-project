"""
#If FastIO not needed, used this and don't forget to strip
#import sys, math
#input = sys.stdin.readline
"""

import os
import sys
from io import BytesIO, IOBase
import heapq as h 
from bisect import bisect_left, bisect_right

from types import GeneratorType
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
 
    def __init__(self, file):
        import os
        self.os = os
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
 
    def read(self):
        while True:
            b = self.os.read(self._fd, max(self.os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
 
    def readline(self):
        while self.newlines == 0:
            b = self.os.read(self._fd, max(self.os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
 
    def flush(self):
        if self.writable:
            self.os.write(self._fd, self.buffer.getvalue())
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

from collections import defaultdict as dd, deque as dq
import math, string

def getInts():
    return [int(s) for s in input().split()]

def getInt():
    return int(input())

def getStrs():
    return [s for s in input().split()]

def getStr():
    return input()

def listStr():
    return list(input())

MOD = 10**9+7

"""
Start with P
P has factors pi**qi
X = P, is X % Q == 0, doesn't work

Need the largest factor of P s.t. factor % Q = 0

30
10
1 2 3 5 6 10 15 30 so 15 is the answer

If P//Q is the smallest factor of P, the answer is the next smallest factor
Otherwise, the answer is either the next factor, or a smaller factor which doesn't divide P//Q

We need to remove a combination of factors from P until it doesn't divide Q any more

50 = 2*2*5
100 = 2*2*5*5

10 = 2*5
30 = 2*3*5

Answer = 5*5

"""
from functools import reduce

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def solve():
    P, Q = getInts()
    if P < Q:
        return P
    if P % Q > 0:
        return P
    facs = sorted(list(factors(Q)))
    best = 0
    for fac in facs:
        if fac == 1:
            continue
        power = 1
        while P % fac**power == 0:
            #print(P,fac,power,flush=True)
            tmp = P//(fac**power)
            if tmp % Q > 0:
                best = max(best,tmp)
            power += 1
    return best
    
for _ in range(getInt()):
    print(solve())