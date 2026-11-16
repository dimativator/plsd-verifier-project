n = int(input())
a = list(map(int, input().split()))

maxLocate = a.index(n)
minLocate = a.index(1)

distanceMax = len(a) - 1 - a.index(n)
distanceMin = len(a) - 1 - a.index(1)

print(max(maxLocate, minLocate, distanceMax, distanceMin))
