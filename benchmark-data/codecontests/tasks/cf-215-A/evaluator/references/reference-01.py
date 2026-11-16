n = int(input())
a = list(map(int,input().split()))
m = int(input())
b = list(map(int,input().split()))
count = []
for i in range(n):
    for j in range(m):
        if((b[j]/a[i])==int(b[j]/a[i])):
            count.append(int(b[j]/a[i]))
o = max(count)
print(count.count(o))
