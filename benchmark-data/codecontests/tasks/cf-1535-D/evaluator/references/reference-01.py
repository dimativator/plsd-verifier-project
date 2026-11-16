# Legends Always Come Up with Solution
# Author: Manvir Singh

import os
import sys
from io import BytesIO, IOBase
def solve(z, dp, s):
    n = len(dp)
    while 1:
        dp[z] = 0
        if s[z] == '?':
            if 2 * z + 1 < n:
                dp[z] += dp[2 * z + 1]
            else:
                dp[z] += 1
            if 2 * z + 2 < n:
                dp[z] += dp[2 * z + 2]
            else:
                dp[z] += 1
        elif s[z] == "1":
            if 2 * z + 1 < n:
                dp[z] += dp[2 * z + 1]
            else:
                dp[z] += 1
        else:
            if 2 * z + 2 < n:
                dp[z] += dp[2 * z + 2]
            else:
                dp[z] += 1
        if not z:
            return
        z = (z - 1) // 2
def main():
    input()
    s = list(input().rstrip())
    s.reverse()
    n = len(s)
    dp = [0] * n
    for i in range(n - 1, -1, -1):
        if s[i] == "?":
            if 2 * i + 1 < n:
                dp[i] += dp[2 * i + 1]
            else:
                dp[i] += 1
            if 2 * i + 2 < n:
                dp[i] += dp[2 * i + 2]
            else:
                dp[i] += 1
        elif s[i] == "1":
            if 2 * i + 1 < n:
                dp[i] += dp[2 * i + 1]
            else:
                dp[i] = 1
        else:
            if 2 * i + 2 < n:
                dp[i] += dp[2 * i + 2]
            else:
                dp[i] = 1
    for i in range(int(input())):
        x, y = input().split()
        x = n - int(x)
        s[x] = y
        solve(x, dp, s)
        print(dp[0])

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