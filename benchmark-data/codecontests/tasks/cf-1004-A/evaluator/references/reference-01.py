n, d = map(int,input().split())
a = list(map(int,input().split()))
count = 0
for i in range(n-1):
    if a[i + 1] - a[i] == 2 * d:
        count +=1
    elif a[i + 1] - a[i] > 2 * d:
        count += 2
print(count + 2)
        