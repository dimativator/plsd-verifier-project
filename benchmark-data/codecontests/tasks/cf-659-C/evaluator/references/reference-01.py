n, m = map(int, input().split())
a = set(map(int, input().split()))
s, z, k = "", 1, 0
while m >= z:
    if z not in a:
        m -= z
        k += 1
        s+=(str(z)+" ")
    z += 1
print(k)
print(s)
