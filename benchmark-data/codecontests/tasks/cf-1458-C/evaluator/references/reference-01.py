import sys,io,os
Z=io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
Y=lambda:[*map(int,Z().split())]
def I(M):
    n=len(M)
    nM=[[0]*n for i in range(n)]
    for x in range(n):
        for y in range(n):
            nM[x][M[x][y]-1]=y+1
    return nM
def C(M):
    n=len(M)
    nM=[[0]*n for i in range(n)]
    for x in range(n):
        for y in range(n):
            nM[M[x][y]-1][y]=x+1
    return nM
def T(M):
    n=len(M)
    nM=[[0]*n for i in range(n)]
    for x in range(n):
        for y in range(n):
            nM[x][y]=M[y][x]
    return nM
o=[]
for _ in range(int(Z())):
    n,m=Y();M=[]
    for i in range(n):M.append(Y())
    s=Z().strip()
    s=s[::-1]
    dx=dy=dv=0
    ui=t=0
    for i in s:
        if ui==67:
            if i==68:i=65
            elif i==85:i=83
            elif i==73:i=84
            elif i==67:ui=i=0
        elif ui==73:
            if i==82:i=65
            elif i==76:i=83
            elif i==67:i=84
            elif i==73:ui=i=0
        if t:
            if i==82:i=68
            elif i==76:i=85
            elif i==68:i=82
            elif i==85:i=76
        if i==82:dx+=1
        elif i==76:dx-=1
        elif i==68:dy+=1
        elif i==85:dy-=1
        elif i==73:ui=73
        elif i==67:ui=67
        elif i==84:t=1-t
        elif i==83:dv-=1
        elif i==65:dv+=1
    if ui==67:M=C(M)
    elif ui==73:M=I(M)
    if t:M=T(M)
    nM=[[0]*n for i in range(n)]
    for x in range(n):
        for y in range(n):
            nM[x][y]=(M[(x-dy)%n][(y-dx)%n]-1+dv)%n+1
    o.append('\n'.join(' '.join(map(str,r))for r in nM))
print('\n\n'.join(o))