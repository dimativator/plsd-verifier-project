k1, k2, k3 = map(int, input().split())
ans = 'NO'
if [k1, k2, k3].count(2) >= 2:
    ans = 'YES'
if 1 in [k1, k2, k3]:
    ans = 'YES'
if [k1, k2, k3].count(3) >= 3:
    ans = 'YES'
if 2 in [k1, k2, k3] and [k1, k2, k3].count(4) == 2:
    ans = 'YES'
print(ans)
