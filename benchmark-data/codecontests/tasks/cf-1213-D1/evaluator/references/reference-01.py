import collections
import functools
import math
import sys
import bisect


def In():
    return map(int, sys.stdin.readline().split())


input = sys.stdin.readline

def eqdiv():
    n,k = In()
    cost = [0]*int(1e5*2+10)
    count = cost[:]
    l = list(In())
    l.sort()
    for i in l:
        i = int(i)
        pos = 0
        while i:
            if count[i] < k:
                count[i] += 1
                cost[i] += pos
            pos += 1
            i //= 2
    ans = float('inf')
    for i in range(len(cost)):
        if count[i] == k and cost[i] < ans:
            ans = min(ans,cost[i])
    return ans
print(eqdiv())

