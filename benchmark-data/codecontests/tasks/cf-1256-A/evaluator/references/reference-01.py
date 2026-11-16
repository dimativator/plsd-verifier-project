from fractions import gcd
from datetime import date, timedelta
from heapq import*
import math
from collections import defaultdict, Counter, deque
import sys
from bisect import *
import itertools
import copy
sys.setrecursionlimit(10 ** 7)
MOD = 10 ** 9 + 7


def main():
    q = int(input())
    for i in range(q):
        a, b, n, s = map(int, input().split())
        
        if s - n * a >= 0:
            s -= n * a
        else:
            s = s - (s//n)*n
            

            
        if s <= b:
            print("YES")
        else:
            print("NO")

        
        
        
            

    
   


if __name__ == '__main__':
    main()
