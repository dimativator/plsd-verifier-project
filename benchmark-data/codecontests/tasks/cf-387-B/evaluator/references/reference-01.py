n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
cnt = 0
j = 0
for i in range(n):
    while j < m:
        if a[i] <= b[j]:
            cnt += 1
            j += 1
            break
        else:
            j += 1
print(n - cnt)
