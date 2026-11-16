n, k = [int(i) for i in input().split()]
s = input()
arr = input().split()


subs = [0]
for x in s:
  if(x in arr): subs[-1] += 1
  else: 
    subs.append(0)

count = 0
for x in subs:
  count += x*(x+1)/2

print(int(count))