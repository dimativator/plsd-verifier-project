n, m = map(int, input().split())
mas = list(map(int, input().split()))
mn = 1001
for i in range(1, n + 1):
    if mas.count(i) < mn:
        mn = mas.count(i)
print(mn)