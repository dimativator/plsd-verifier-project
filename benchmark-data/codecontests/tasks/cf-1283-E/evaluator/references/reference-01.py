# cook your dish here
n = int(input())
f = list(map(int, input().split()))
f.sort()
f1 = []
for i in range(n):
    f1.append(f[i])
    
if (f1[0] > 0):
    f1[0] -= 1
    
for i in range(1, n):
    if (f1[i]-f1[i-1] > 1):
        f1[i] -= 1
    elif (f1[i] == f1[i-1]):
        if (i == n-1 or f1[i+1] > f1[i]):
            f1[i] += 1
        
for i in range(1, n):
    if (f[i]-f[i-1] <= 2):
        f[i] = f[i-1]

max_count = 1
min_count = 1
for i in range(1, n):
    if (f1[i] != f1[i-1]):
        max_count += 1
    if (f[i] != f[i-1]):
        min_count += 1
        
print(min_count, max_count)
        