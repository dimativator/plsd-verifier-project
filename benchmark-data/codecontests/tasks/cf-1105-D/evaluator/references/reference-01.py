# ------------------- fast io --------------------
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

# ------------------- fast io --------------------
from math import gcd, ceil

def pre(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


def prod(a):
    ans = 1
    for each in a:
        ans = (ans * each)
    return ans

def lcm(a, b): return a * b // gcd(a, b)


def binary(x, length=16):
    y = bin(x)[2:]
    return y if len(y) >= length else "0" * (length - len(y)) + y

from collections import deque

for _ in range(int(input()) if not True else 1):
    n, m, pp = map(int, input().split())
    #a, b = map(int, input().split())
    #c, d = map(int, input().split())
    s = list(map(int, input().split()))
    #b = list(map(int, input().split()))
    #s = input()
    a = ['']*n
    ans = [0]*pp
    occupied = [[False]*m for __ in range(n)]
    for i in range(n):
        a[i] = input()

    queues = [deque([]) for __ in range(pp)]
    qc = list(queues)
    for i in range(n):
        for j in range(m):
            dig = a[i][j].isdigit()
            if dig:
                ans[int(a[i][j]) - 1] += 1
                queues[int(a[i][j])-1].append(i*m + j + 1)
                occupied[i][j] = True
            if a[i][j] == '#':
                occupied[i][j] = True

    cur = 0
    while True:
        i = cur % pp
        count = 0
        while count < s[i] and queues[i]:
            lq = len(queues[i])
            for ___ in range(lq):
                x = queues[i][0]
                queues[i].popleft()
                p, q = (x-1) // m, (x-1) % m
                if p != 0 and not occupied[p-1][q]:
                    queues[i].append((p-1)*m+q+1)
                    occupied[p-1][q] = True
                    ans[i] += 1
                if p != n - 1 and not occupied[p+1][q]:
                    queues[i].append((p + 1) * m + q + 1)
                    occupied[p + 1][q] = True
                    ans[i] += 1
                if q != 0 and not occupied[p][q-1]:
                    queues[i].append(p*m + q)
                    occupied[p][q-1] = True
                    ans[i] += 1
                if q != m-1 and not occupied[p][q+1]:
                    queues[i].append(p*m + q + 2)
                    occupied[p][q+1] = True
                    ans[i] += 1
            count += 1
        cur += 1
        pos = True
        for i in queues:
            if i:
                pos = False
                break
        if pos:break

    print(*ans)