n = int(input())
r = lambda : list(map(int, input().split()))
arr = []
for i in range(n):
    a = r()
    arr.append(a)


row = [sum(i) for i in arr]

col = []
for i in range(n):
    c = 0
    for j in range(n): c+=arr[j][i]
    col.append(c)


ans = 0
for i in range(n):
    for j in range(n):
        if row[i] < col[j]: ans+=1

print(ans)
