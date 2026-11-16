import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
from random import *
T = int(input())
ans = [0]*T
for t in range(T):
  X,Y = [0]*4,[0]*4
  A = [0]*4
  for i in range(4):
    X[i],Y[i] = map(int, input().split())
    # X[i], Y[i] = choices(range(1,11),k=2)
    # print(X[i],Y[i])
    A[i] = [X[i], Y[i]]
  X.sort(); Y.sort(); A.sort()
  cnt = 0
  for i in range(2):
    rank = 1
    for j in range(4):
      if A[i][1] < A[j][1]:
        rank += 1
    if rank<=2:
      cnt += 1
  if cnt!=1:
    ans[t] += min(Y[2]-Y[1], X[2]-X[1])*2
  x_min = X[2]-X[1]; x_max = X[3]-X[0]
  y_min = Y[2]-Y[1]; y_max = Y[3]-Y[0]
  if x_max<y_min:
    ans[t] += (X[3]-X[2])+(X[1]-X[0])
    ans[t] += (Y[3]-Y[2])+(Y[1]-Y[0])+2*(y_min-x_max)
  elif y_max<x_min:
    ans[t] += (X[3]-X[2])+(X[1]-X[0])+2*(x_min-y_max)
    ans[t] += (Y[3]-Y[2])+(Y[1]-Y[0])
  else:
    ans[t] += (X[3]-X[2])+(X[1]-X[0])
    ans[t] += (Y[3]-Y[2])+(Y[1]-Y[0])
  # print(ans[t])
print(*ans, sep='\n')