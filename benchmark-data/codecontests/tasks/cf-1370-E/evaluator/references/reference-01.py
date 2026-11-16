# -*- coding: utf-8 -*-
"""
@author: Saurav Sihag
"""

rr = lambda: input().strip()
# rri = lambda: int(rr())
rri = lambda: int(stdin.readline())
rrm = lambda: [int(x) for x in rr().split()]
# stdout.write(str()+'\n')

from sys import stdin, stdout

def sol():
    n=rri()
    s=rr()
    t=rr()
    cnt=0
    mn=0
    mx=0
    for i in range(n):
        if (s[i]=='1'):
            cnt+=1
        if (t[i]=='1'):
            cnt-=1
        mn=min(mn, cnt)
        mx=max(mx, cnt)
    if cnt!=0:
        print(-1)
    else:
        print(mx-mn)
    return

sol()
# T = rri()
# for t in range(1, T + 1):
#     ans = sol()
    # print("Case #{}: {}".format(t, ans))

