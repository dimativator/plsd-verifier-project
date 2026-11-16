#region Header
#!/usr/bin/env python3
# from typing import *

import sys
import io
import math
import collections
import decimal
import itertools
import bisect
import heapq


def input():
    return sys.stdin.readline()[:-1]


# sys.setrecursionlimit(1000000)
#endregion

# _INPUT = """4
# 18
# 6 6 5 4 3 3 3 2 3 5 2 10 7 6 1 1 10 2
# 7
# 1 4 2 2 2 2 2
# 2
# 2 3
# 5
# 1 1 1 1 1
# """
# sys.stdin = io.StringIO(_INPUT)


def solve(N, S):
    n = 0
    T = [0] * N
    for i in range(N):
        if S[i]-1 > T[i]:
            n += S[i]-1 - T[i]
            T[i] += (S[i]-1-T[i])
        if i+S[i] > N:
            a = (N-i) - S[i]
            T[i] = max(T[i] + a, 0)
            S[i] += a
        while T[i] > 0:
            if S[i] == 1:
                if i+1 >= N:
                    break
                T[i+1] += T[i]
                T[i] = 0
                break
            else:
                j = i + S[i]
                if j < N:
                    T[j] += 1
                S[i] -= 1
                T[i] -= 1

    return n

def main():
    T0 = int(input())
    for _ in range(T0):
        N = int(input())
        S = list(map(int, input().split()))
        ans = solve(N, S)
        print(ans)

if __name__ == '__main__':
    main()