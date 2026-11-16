import os
from io import BytesIO, IOBase
import sys
from collections import defaultdict, deque, Counter
from bisect import *
from math import sqrt, pi, ceil, log, inf,gcd
from itertools import permutations
from copy import deepcopy
from heapq import *
from sys import setrecursionlimit
def main():
    q, x = map(int, input().split())
    j = 0
    b = []
    heapify(b)
    c={}
    for i in range(q):
        y = int(input())
        if y == j:
            j += 1
            while len(b) != 0:
                z = heappop(b)
                if z != j:
                    heappush(b, z)
                    break
                j += 1
        else:
            t = abs(j - y)
            if t % x == 0:
                j += 1
                while len(b) != 0:
                    z = heappop(b)
                    if z != j:
                        heappush(b, z)
                        break
                    j += 1
            else:
                z=(y-(t//x)*x if y>j else  y+(t//x+1)*x)
                if c.get(z)==None:
                    c[z]=z+x
                else:
                    a=[]
                    while c.get(z)!=None:
                        a.append(z)
                        z=c[z]
                    a.append(z)
                    for i in a:
                        c[i]=z+x
                heappush(b,z)
        print(j)

# region fastio
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

if __name__ == "__main__":
    main()