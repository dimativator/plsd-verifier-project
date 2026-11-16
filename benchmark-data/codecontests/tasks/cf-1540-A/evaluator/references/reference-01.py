t = int(input())
for _ in range(t):
  n = int(input())
  a = list(map(int,input().split()))
  a = sorted(a)
  b = []
  for i in range(1,n):
    b += [a[i] - a[i-1]]
  ans = 0
  n = len(b)
  for i in range(n):
    ans -= (n-i)*(i+1)*(b[i])
  print(ans + sum(b))