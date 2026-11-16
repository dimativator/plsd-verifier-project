import os
import sys
from io import BytesIO, IOBase


def main():
    import bisect
    import math
    # import itertools
    # import heapq
    # from queue import PriorityQueue, LifoQueue, SimpleQueue

    # import sys.stdout.flush() use for interactive problems
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    inf = 1e17
    mod = 10 ** 9 + 7

    Max = 10 ** 6
    primes = []
    prime = [True for i in range(Max + 1)]
    p = 2
    while (p * p <= Max + 1):

        # If prime[p] is not
        # changed, then it is a prime
        if (prime[p] == True):

            # Update all multiples of p
            for i in range(p * p, Max + 1, p):
                prime[i] = False
        p += 1

    for p in range(2, Max + 1):
        if prime[p]:
            primes.append(p)

    def factorial(n):
        f = 1

        for i in range(1, n + 1):
            f = (f * i) % mod  # Now f never can
        # exceed 10^9+7

        return f

    def ncr(n, r):
        # initialize numerator
        # and denominator
        num = den = 1
        for i in range(r):
            num = (num * (n - i)) % mod
            den = (den * (i + 1)) % mod
        return (num * pow(den,
                          mod - 2, mod)) % mod

    def solve(n,arr):

        chance = [0]*(n+1)
        chance[-2] = arr[-1]
        for i in range(n-2,-1,-1):
            chance[i] = max(chance[i+1],sum(arr[i+1:])-chance[i+1]+arr[i])

        #print(chance)
        return sum(arr)-chance[0],chance[0]

















        pass

    t = 1# int(input())
    ans = []
    for _ in range(t):
        n = int(input())
        # x = int(input())
        # y = int(input())
        # n,k = map(int, input().split())
        arr = [int(x) for x in input().split()]
        #arr2 = [int(x) for x in input().split()]
        # arr = list(input())
        # s = input()
        # t = input()
        # grid = []
        # for i in range(n):
        #     grid.append([int(x) for x in input().split()])
        # arr = []
        # for j in range(n):
        #     arr.append(int(input()))

        ans.append(solve(n,arr))

    for j in range(len(ans)):
        # print('Case #' + str(j + 1) + ": " + str(ans[j]))
        print(ans[j][0],ans[j][1])

    pass


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

# endregion

if __name__ == "__main__":
    main()
