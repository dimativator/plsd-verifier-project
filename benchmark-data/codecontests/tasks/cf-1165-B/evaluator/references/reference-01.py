a = int(input())
b = [int(x) for x in input().split()]
b.sort()
s = 1
q = 0
for i in b:
  if i >= s:
    s += 1
    q += 1
print(q)