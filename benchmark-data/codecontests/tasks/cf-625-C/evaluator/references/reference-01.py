n, k = [int(x) for x in input().split(' ')]
ans = 0
y = n*(k-1)+1
x = 1
barr = []
for i in range(n):
    arr = []
    for j in range(k-1):
        arr.append(x)
        x += 1
    for j in range(k-1, n):
        arr.append(y)
        y += 1
    ans += arr[k-1]
    barr.append(' '.join(map(str, arr)))
print(ans)
print('\n'.join(barr))