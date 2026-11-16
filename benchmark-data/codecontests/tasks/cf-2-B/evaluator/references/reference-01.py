# Legends Always Come Up with Solution
# Author: Manvir Singh

import os
from io import BytesIO, IOBase
import sys
from collections import defaultdict, deque, Counter
from math import sqrt, pi, ceil, log, inf, gcd, floor
from itertools import combinations, permutations
from bisect import *
from fractions import Fraction
from heapq import *
from random import randint

def solve(x,y):
    z=0
    while not x%y and x!=0:
        z+=1
        x=x//y
    return z

def main():
    n = int(input())
    m_2 = [list(map(int, input().split())) for _ in range(n)]
    m_5 = [[0 for _ in range(n)] for _ in range(n)]
    x = (-1, -1)
    for i in range(n):
        for j in range(n):
            if m_2[i][j] == 0:
                x = (i, j)
                break
        if x[0] != -1:
            break
    m_2[0][0], m_5[0][0] = solve(m_2[0][0], 2), solve(m_2[0][0], 5)
    for i in range(1, n):
        m_5[0][i], m_2[0][i] = m_5[0][i - 1] + solve(m_2[0][i], 5), m_2[0][i - 1] + solve(m_2[0][i], 2)
        m_5[i][0], m_2[i][0] = m_5[i - 1][0] + solve(m_2[i][0], 5), m_2[i - 1][0] + solve(m_2[i][0], 2)
    for i in range(1, n):
        for j in range(1, n):
            m_5[i][j] = min(m_5[i - 1][j], m_5[i][j - 1]) + solve(m_2[i][j], 5)
            m_2[i][j] = min(m_2[i - 1][j], m_2[i][j - 1]) + solve(m_2[i][j], 2)
    if min(m_5[-1][-1], m_2[-1][-1]) > 1 and x[0] != -1:
        print(1)
        print("R" * (x[1]) + "D" * (n - 1) + "R" * (n - x[1] - 1))
    else:
        global c
        if m_5[-1][-1] < m_2[-1][-1]:
            c = m_5
        else:
            c = m_2
        b, i, j = [], n - 1, n - 1
        while i or j:
            if i - 1 >= 0 and j - 1 >= 0:
                if c[i - 1][j] < c[i][j - 1]:
                    b.append("D")
                    i -= 1
                else:
                    b.append("R")
                    j -= 1
            elif i == 0:
                b.append("R")
                j -= 1
            else:
                b.append("D")
                i -= 1
        print(c[-1][-1])
        b.reverse()
        print("".join(b))


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