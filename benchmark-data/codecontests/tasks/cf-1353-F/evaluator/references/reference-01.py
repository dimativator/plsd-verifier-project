#!/usr/bin/env python
import os
import sys
from io import BytesIO, IOBase


def main():
    for _ in range(int(input())):
        n,m=map(int,input().split())
        a=[ [int(x) for x in input().split()] for _ in range(n)]
        if m>n:
            b=[ [a[j][i] for j in range(n)] for i in range(m)]    
            a=b
            n,m=m,n
        # print(a,n,m)
        for i in range(n):
            for j in range(m):
                a[i][j]-=i+j
        # print(a)
        # print(d)
        from collections import defaultdict
        pvr=[defaultdict(lambda: 1<<67) for _ in range(m)]
        # print(a)
        for i in range(n):
            cur=[defaultdict(lambda: 1<<67) for _ in range(m)]
            for j in range(m):
                if i==0:
                    cur[0][a[0][0]]=0
                if i:
                    for k,v in pvr[j].items():
                        if k<=a[i][j]:
                            cur[j][k]=min(cur[j][k],v+a[i][j]-k)
                        else:
                            cur[j][a[i][j]]=min(cur[j][a[i][j]],v+(k-a[i][j])*(i+j))                        
                if j:
                    for k,v in cur[j-1].items():
                        if k<=a[i][j]:
                            cur[j][k]=min(cur[j][k],v+a[i][j]-k)
                        else:
                            cur[j][a[i][j]]=min(cur[j][a[i][j]],v+(k-a[i][j])*(i+j))
                # print(i,j,cur[j])
            pvr=cur
        ans=1<<63
        for k,v in pvr[-1].items():
            # print("kv",k,v)
            ans=min(ans,v)
        print(ans)
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