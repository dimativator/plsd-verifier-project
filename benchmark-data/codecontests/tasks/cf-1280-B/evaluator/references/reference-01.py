"""
    This template is made by Satwik_Tiwari.
    python programmers can use this template :)) .
"""

#===============================================================================================
#importing some useful libraries.

import sys
import bisect
import heapq
from math import *
from collections import Counter as counter  # Counter(list)  return a dict with {key: count}
from itertools import combinations as comb # if a = [1,2,3] then print(list(comb(a,2))) -----> [(1, 2), (1, 3), (2, 3)]
from itertools import permutations as permutate
from bisect import bisect_left as bl #
from bisect import bisect_right as br
from bisect import bisect

#===============================================================================================
#some shortcuts

mod = pow(10, 9) + 7
def inp(): return sys.stdin.readline().strip() #for fast input
def out(var): sys.stdout.write(str(var))  #for fast output, always take string
def lis(): return list(map(int, inp().split()))
def stringlis(): return list(map(str, inp().split()))
def sep(): return map(int, inp().split())
def strsep(): return map(str, inp().split())
def graph(vertex): return [[] for i in range(0,vertex+1)]
def zerolist(n): return [0]*n
def nl(): out("\n")  #as stdout.write always print sring.
def testcase(t):
    for p in range(t):
        solve()
def printlist(a) :
    for p in range(0,len(a)):
        out(str(a[p]) + ' ')
def lcm(a,b): return (a*b)//gcd(a,b)


#===============================================================================================
# code here ;))

def solve():
    n,m = sep()
    a = []
    f0 = True
    imp = True
    for i in range(0,n):
        temp = list(inp())
        if(temp.count('A') < m):
            f0 = False
        if(temp.count('A') > 0):
            imp = False
        a.append(temp)
    if(imp):
        print('MORTAL')
    elif(f0):
        print(0)
    else:
        col = []
        for j in range(0,m):
            temp = []
            for i in range(0,n):
                temp.append(a[i][j])
            col.append(temp)

        if(a[0].count('A')==m or a[n-1].count('A')==m or col[m-1].count('A')==n or col[0].count('A')==n):
            print(1)
        else:
            f1 = False
            f2 = False
            f3 = False
            cnt = 0
            for i in range(0,n):
                cnt = max(cnt,a[i].count('A'))
            if(cnt==m):
                f1 = True
            cnt = 0
            for i in range(0,m):
                cnt = max(cnt,col[i].count('A'))
            if(cnt==n):
                f2 = True
            if(a[0][0]=='A' or a[0][m-1]=='A' or a[n-1][0]=='A' or a[n-1][m-1]=='A'):
                f3 = True
            if(f1 or f2 or f3):
                print(2)
            else:
                if(a[0].count('A')>0 or a[n-1].count('A')>0 or col[0].count('A')>0 or col[m-1].count('A')>0):
                    print(3)
                else:
                    print(4)



testcase(int(inp()))
# testcase(1)













