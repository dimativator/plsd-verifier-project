# from __future__ import print_function,division
# range = xrange
import sys
input = sys.stdin.readline
# sys.setrecursionlimit(10**9)
from sys import stdin, stdout
from collections import defaultdict, Counter
M = 10**9+7

def main():
    for _ in range(int(input())):
        n = int(input())
        s = input().strip()
        w = 0
        os = 0
        mid = 0
        for i in range(n//2):
            if s[i]!=s[n-i-1]:
                w+=1
            elif s[i]=="0":
                os+=2
        if n%2 and s[n//2]=='0':
            mid = 1
        if w==0:
            if mid==1 and os==0:
                print("BOB")
            elif mid==1:
                print("ALICE")
            else:
                print("BOB")
        elif w==1:
            if mid==1:
                if os==0:
                    print("DRAW")
                else:
                    print("ALICE")
            else:
                print("ALICE")
        else:
            print("ALICE")

if __name__== '__main__':
    main()