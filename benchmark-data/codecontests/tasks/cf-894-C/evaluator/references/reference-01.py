from math import gcd
m = int(input())
s = [int(i) for i in input().split()]
gc = s[0]
for i in range(0,m):
    gc = gcd(gc,s[i])
if gc not in s:
    print(-1)
else:
    print(2*m-1)
    ans = [s[0]]*(2*m-1)
    cur = 1
    for i in range(2,2*m-1,2):
        ans[i] = s[cur]
        cur += 1
    print(*ans)

"""
3
1 10 15
"""