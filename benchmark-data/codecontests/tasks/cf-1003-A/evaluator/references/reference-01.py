n = int(input())
mn = list(map(int, input().split()))
k = 1
for i in range(1, 101):
    s = mn.count(i)
    if s > k:
        k = s
print(k)