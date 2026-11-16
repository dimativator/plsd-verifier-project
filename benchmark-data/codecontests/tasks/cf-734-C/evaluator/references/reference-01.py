"""
ref: http://codeforces.com/blog/entry/48397
At first, observe that if we'll take the i-th potion of the first type and
the j-th potion of the second type, then we can prepare all the potions in
ai*(n-cj) seconds. So, we have to minimize this number.

Let's iterate over what potion of the first type we'll use. Then we must find
such spell of the second type that will prepare instantly as many as possible
potions, and we'll have enough manapoints for it. It can be done using binary search,
because the characteristics of potions of the second type — ci and di are sorted
in non-decreasing order.

Time complexity is O(mlogk + k).
"""

import bisect
import sys

a = b = c = d = []

n,m,k = [ int(i) for i in input().split() ]
x,s = [ int(i) for i in input().split() ]

ans = n * x

a = [ int(i) for i in input().split() ]
b = [ int(i) for i in input().split() ]
c = [ int(i) for i in input().split() ]
d = [ int(i) for i in input().split() ]

a.append(x)
b.append(0)
for i in range(m+1):
        if b[i]>s:
                continue
        if s-b[i]<d[0]:
                ans = min(ans, a[i]*n)
                continue

        #t = bisect.bisect_right(d, s-b[i], 0, len(d)) -1
        t = bisect.bisect_right(d, s-b[i], 0, k) -1
        ans = min(ans, (n-c[t])*a[i])

print(ans)

