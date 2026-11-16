import sys
import math
import bisect
from sys import stdin, stdout
from math import gcd, floor, sqrt, log2, ceil
from collections import defaultdict
from bisect import bisect_left as bl, bisect_right as br
from collections import Counter
from collections import deque
 
ip = lambda : int(stdin.readline())
inp = lambda: map(int,stdin.readline().split())
ips = lambda: stdin.readline().rstrip()

t = ip()
for _ in range(t):
    n,m = inp()
    if n == 1 or m == 1:
        print("YES")
    elif n == 2 and m == 2:
        print("YES")
    else:
        print("NO")
            
        
