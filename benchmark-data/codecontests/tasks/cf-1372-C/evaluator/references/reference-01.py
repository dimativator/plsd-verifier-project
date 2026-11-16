import sys
import math
import heapq
import collections
def inputnum():
    return(int(input()))
def inputnums():
    return(map(int,input().split()))
def inputlist():
    return(list(map(int,input().split())))
def inputstring():
    return([x for x in input()])
def inputmatrixchar(rows):
    arr2d = [[j for j in input().strip()] for i in range(rows)] 
    return arr2d
def inputmatrixint(rows):
    arr2d = []
    for _ in range(rows):
        arr2d.append([int(i) for i in input().split()])
    return arr2d
    
t=int(input())
for q in range(t):
    n = inputnum()
    a = inputlist()
    wrong = 0
    firstwrong = False
    secondwrong = False
    for i in range(n):
        if i+1 != a[i]:
            if not firstwrong:
                firstwrong = True
            elif firstwrong and a[i-1] == i and i > 1:
                secondwrong = True
            wrong += 1 
        
    if wrong == 0:
        print(0)
    elif not secondwrong:
        print(1)
    else:
        print(2)