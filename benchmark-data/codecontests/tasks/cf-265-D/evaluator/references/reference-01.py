# Legends Always Come Up with Solution
# Author: Manvir Singh

import os
import sys
from io import BytesIO, IOBase
from collections import Counter

def seieve_prime_factorisation(n):
    p, i = [1] * (n + 1), 2
    while i * i <= n:
        if p[i] == 1:
            for j in range(i * i, n + 1, i):
                p[j] = i
        i += 1
    return p

def prime_factorisation_by_seive(p, x):
    c = Counter()
    while p[x] != 1:
        c[p[x]] += 1
        x = x // p[x]
    c[x] += 1
    return c

def main():
    n=int(input())
    a=list(map(int,input().split()))
    p=seieve_prime_factorisation(max(a))
    dp=[1]*n
    b=Counter()
    for i in range(n-1,-1,-1):
        z=prime_factorisation_by_seive(p,a[i])
        ma=0
        for j in z:
            ma=max(ma,b[j])
        dp[i]+=ma
        for j in z:
            b[j]=max(b[j],dp[i])
    print(max(dp))

# (region fastio
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