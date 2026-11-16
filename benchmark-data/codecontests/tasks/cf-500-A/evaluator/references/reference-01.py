a, b = map(int, input().split())
c = list(map(int, input().split()))
d = 0
while d < b - 1:
    d += c[d]
if d == b - 1:
    print("YES")
else:
    print("NO")