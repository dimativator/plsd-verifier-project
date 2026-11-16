# Problem Link :- https://codeforces.com/contest/1400/problem/D

import sys
input = sys.stdin.readline

############ ---- Input Functions ---- ############
def inp():
    return(int(input()))
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input()
    return(list(s[:len(s) - 1]))
def invr():
    return(map(int,input().split()))

def solve(arr,n):
    cntLeft = dict()
    cntRight = dict()
    res = 0
    for j in range(n):
        cntRight = dict()
        for k in range(n-1,j,-1):
            res += (cntLeft.get(arr[k],0) * cntRight.get(arr[j],0))
            if arr[k] not in cntRight:
                cntRight[arr[k]] = 1
            else:
                cntRight[arr[k]] += 1
        if arr[j] not in cntLeft:
            cntLeft[arr[j]] = 1
        else:
            cntLeft[arr[j]] += 1
    return res

t = inp()
while t > 0:
    n = inp()
    arr = inlt()
    print(solve(arr,n))
    t -= 1