
n = (input()).split()
l = int(n[0])
r = int(n[1])
a = []
x = []
a.append([])
a[0].append('4')
a[0].append('7')

for i in range(1,10):
    a.append([])
    for j in a[i-1]:
        
        a[i].append('4'+j)
        a[i].append('7'+j)
    for j in a[i]:
        x.append(int(j))
x.append(4)
x.append(7)
x.sort()
sum = [16]
for i in range(1,len(x)):
    sum.append((x[i]-x[i-1])*x[i]+sum[i-1])
for i in range(len(x)):
    if x[i] >= l:
        t = i 
        break
for i in range(len(x)):
    if x[i] >= r:
        e  = i
        break
res = sum[e] - sum[t] - x[e] * (x[e]-r) + (x[t]-l+1) * x[t]
print(res)

