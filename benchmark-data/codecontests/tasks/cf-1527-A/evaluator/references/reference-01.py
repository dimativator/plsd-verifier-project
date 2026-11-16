from math import log
from math import floor
t = int(input())

for i in range(t):
    n = int(input())
    #print(n)
    k = 2**(floor(log(n,2)))-1
    print(k)

