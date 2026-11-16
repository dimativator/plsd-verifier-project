n,l = map(int,input().split())

kefa = list(map(int,input().split()))

sasha = list(map(int,input().split()))

diff1 = [kefa[i+1] - kefa[i] if i != n - 1 else l - kefa[-1] + kefa[0]  for i in range(n) ]

diff2 = [sasha[i+1] - sasha[i] if i != n - 1 else l - sasha[-1] + sasha[0]  for i in range(n) ]



def rotation(pos):
  for i in range(n):
    if diff2[(i+pos)%n] != diff1[i]:
      return False
  return True
  
for i in range(n):
  if(rotation(i)):
    print("YES")
    exit()

print("NO")
  
    