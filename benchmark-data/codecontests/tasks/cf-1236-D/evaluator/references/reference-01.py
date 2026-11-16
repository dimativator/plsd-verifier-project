from sys import stdout
printn = lambda x: stdout.write(x)
inn = lambda : int(input())
inl   = lambda: list(map(int, input().split()))
inm   = lambda:      map(int, input().split()) 
DBG = True  and False
BIG = 999999999
R = 10**9 + 7

def ddprint(x):
  if DBG:
    print(x)

n,m,k = inm() 
hx = {}
hy = {}
cnt = 0
for i in range(k):
  x,y = inm()
  x -= 1
  y -= 1
  cnt += 1
  if x in hx:
    hx[x].append(y)
  else:
    hx[x] = [y]
  if y in hy:
    hy[y].append(x)
  else:
    hy[y] = [x]

ddprint(hx)
ddprint(hy)
x,y = 0,0
dir = 1
if m==1 or (m>1 and 0 in hx and 1 in hx[0]):
  dir = 2
minx = miny = -1
maxx = n
maxy = m
while True:
  #ddprint("x {} y {} dir {} mn {} {} mx {} {}".format(x,y,dir,minx,miny,maxx,maxy))
  nx = x
  ny = y

  if dir==1:
    a = [z for z in hx[x] if y<z and z<maxy] if x in hx else []
    #ddprint(a)
    if len(a)==0:
      ny = maxy-1
    else:
      a.sort()
      ny = a[0]-1
    if ny==y:
        break
    cnt += ny-y
    y = ny
    minx = x
    dir = 2

  elif dir==2:
    a = [z for z in hy[y] if x<z and z<maxx] if y in hy else []
    if len(a)==0:
      nx = maxx-1
    else:
      a.sort()
      nx = a[0]-1
    if nx==x:
        break
    cnt += nx-x
    x = nx
    maxy = y
    dir = 3

  elif dir==3:
    a = [z for z in hx[x] if miny<z and z<y] if x in hx else []
    if len(a)==0:
      ny = miny+1
    else:
      a.sort(reverse=True)
      ny = a[0]+1
    if ny==y:
        break
    cnt += y-ny
    y = ny
    maxx = x
    dir = 4

  elif dir==4:
    a = [z for z in hy[y] if minx<z and z<x] if y in hy else []
    if len(a)==0:
      nx = minx+1
    else:
      a.sort(reverse=True)
      nx = a[0]+1
    if nx==x:
        break
    cnt += x-nx
    x = nx
    miny = y
    dir = 1

print('Yes' if cnt==n*m-1 else 'No')
