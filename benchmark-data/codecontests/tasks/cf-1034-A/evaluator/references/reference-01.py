from math import gcd
n = int(input())
l = list(map(int,input().split()))
m = max(l)+1
prime = [0]*(m)
commondivisor = [0]*(m)

def seive():
  for i in range(2,m):
    if prime[i] == 0:
      for j in range(i*2,m,i):
        prime[j] = i

  for i in range(2,m):
    if not prime[i]:
      prime[i] = i


gc = l[0]
for i in range(1,n):
  gc = gcd(gc,l[i])

seive()

mi = -1
for i in range(n):
  ele = l[i]//gc
  while ele > 1:
    div = prime[ele]
    commondivisor[div]+=1

    while ele%div == 0:
      ele //= div
    
    mi = max(mi,commondivisor[div])


if mi == -1:
  print(-1)
else:
  print(n-mi)