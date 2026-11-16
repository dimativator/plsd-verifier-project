t = int(input())
for _ in range(t):
  n = int(input())
  a = list(int(x) for x in input().split())
  start = 0
  end = n-1
  while end>0 and a[end]<=a[end-1]:
    end-=1
  start=end
  while start>0 and a[start]>=a[start-1]:
    start-=1
  print(start)

