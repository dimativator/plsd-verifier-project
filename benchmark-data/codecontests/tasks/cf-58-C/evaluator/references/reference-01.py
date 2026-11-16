from collections import defaultdict as dd

n = int(input())
a = list(map(int, input().split()))
count = dd(lambda: 0)
for i in range(n//2):
    count[a[i]-i] += 1
    count[a[n-i-1] - i] += 1
    #print(i, a[i]-i, a[n-i-1]-i)
#print([count[k] for k in count.keys()])
if n%2: count[a[n//2]-n//2] += 1
print(n - max([count[k] for k in count.keys() if k > 0]))