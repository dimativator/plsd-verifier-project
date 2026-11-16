n = int(input())
a = [0] * 601
for x in input().split():
    a[int(x)] = 1
a[0] = 0
print(sum(a))
