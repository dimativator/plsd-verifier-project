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

# _INPUT = """# paste here...
# """
# sys.stdin = io.StringIO(_INPUT)



def solve(S):
    Move = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}
    Moves = [Move[c] for c in S]
    pos1 = (0, 0)
    for k in range(len(S)):
        pos1 = (pos1[0] + Moves[k][0], pos1[1] + Moves[k][1])
        block = pos1
        pos = (0, 0)
        for i in range(len(S)):
            pos_next = (pos[0] + Moves[i][0], pos[1] + Moves[i][1])
            if pos_next != block:
                pos = pos_next
        if pos == (0, 0):
            return block
    return (0, 0)

def main():
    T0 = int(input())
    for _ in range(T0):
        S = input()
        ans = solve(S)
        print(*ans)

if __name__ == '__main__':
    main()
