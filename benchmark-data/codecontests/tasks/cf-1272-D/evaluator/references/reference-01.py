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

n=int(input())
vals=list(map(int,input().split()))
#find the continous increasing
chain=1
chains=[]
left=0
right=0
for s in range(1,n):
    if vals[s]>vals[s-1]:
        chain+=1
        right=s
    else:
        if chain>=1:
            chains.append((left,right))
        left=s
        right=s
        chain=1
if len(chains)>0:
    if chains[-1][1]!=n-1:
        chains.append((left,right))
else:
    chains.append((left,right))
#then we loop throughthe chains
length=0
if len(chains)>=2:
    for s in range(len(chains)):
        int1=chains[s]
        #we need to look at
        need=int1[0]-2
        if need>=0:
            int2=chains[s-1]
            if int2[0]<=need and need<=int2[1]:
                if vals[need]<vals[int1[0]]:
                    d1=(int1[1]+1-int1[0])+(need+1-int2[0])
                    if d1>length:
                        length=d1
                else:
                    d1=int1[1]+1-int1[0]
                    if d1>length:
                        length=d1
            else:
                int3=chains[s-2]
                if int3[0]<=need and need<=int3[1]:
                    if vals[need]<vals[int1[0]]:
                        d1=(int1[1]+1-int1[0])+(need+1-int3[0])
                        if d1>length:
                            length=d1
                    else:
                        d1=int1[1]+1-int1[0]
                        if d1>length:
                            length=d1
                else:
                    d1=int1[1]+1-int1[0]
                    if d1>length:
                        length=d1
        else:
            d1=int1[1]+1-int1[0]
            if d1>length:
                length=d1
        need1=int1[1]+2
        if need1<=len(vals)-1:
            int2=chains[s+1]
            if int2[0]<=need1 and need1<=int2[1]:
                if vals[int1[1]]<vals[need1]:
                    d1=(int2[1]+1-need1)+(int1[1]+1-int1[0])
                    if d1>length:
                        length=d1
                else:
                    d1=int1[1]+1-int1[0]
                    if d1>length:
                        length=d1
            else:
                int3=chains[s+2]
                if int3[0]<=need1 and need1<=int3[1]:
                    if vals[int1[1]]<vals[need1]:
                        d1=(int3[1]+1-need1)+(int1[1]+1-int1[0])
                        if d1>length:
                            length=d1
                    else:
                        d1=int1[1]+1-int1[0]
                        if d1>length:
                            length=d1
                else:
                    d1=int1[1]+1-int1[0]
                    if d1>length:
                        length=d1
        else:
            d1=int1[1]+1-int1[0]
            if d1>length:
                length=d1
            
else:
    length=chains[0][1]+1-chains[0][0]
print(length)