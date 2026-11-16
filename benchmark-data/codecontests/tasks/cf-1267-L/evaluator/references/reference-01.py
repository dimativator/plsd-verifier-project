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
n,l,k=map(int,input().split())
vals=[ord(s) for s in input()];vals.sort(reverse=True)
slots=[[] for s in range(n)]
if k==1:
    while len(slots[k-1])<l:
        slots[k-1].append(vals.pop())
    for s in range(l):
        for i in range(n):
            if len(slots[i])<l:
                slots[i].append(vals.pop())
else:
    ind=0
    for s in range(l):
        for i in range(ind,k):
            slots[i].append(vals.pop())
        #we'll update the index as we go
        for i in range(1,k):
            if slots[i-1][-1]<slots[i][-1]:
                ind=i
                if i==k-1:
                    break
    while len(slots[k-1])<l:
        slots[k-1].append(vals.pop())
    for s in range(l):
        for i in range(n):
            if len(slots[i])<l:
                slots[i].append(vals.pop())
for i in slots:
    ans=[chr(b) for b in i]
    print("".join(ans))