import sys
import math

n = int(input())

l = 1
r = 2*n

while(l < r):
    candies = n
    numeaten = 0
    k = (l+r)//2
#    print(k)
    while(candies > 0):
        if candies > k:
            numeaten += k
            candies -= k
        else:
            numeaten += candies
            break
        c = candies//10
        candies -= c
    if numeaten < (n+1)//2:
#        print(n, end = ' ')
#        print(n//2)
        l = k+1
    else:
        r = k

print(l)
