from sys import stdin, stdout
import collections
import math
import heapq

def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3,n,2) if sieve[i]]
 
 
p = primes(2750132)

look_up = {}
 
i = 1
for num in p:
    look_up[num] = i
    i += 1

N = int(input())
#N,M = [int(x) for x in stdin.readline().split()] 

arr = [int(x) for x in stdin.readline().split()]

arr.sort()

h = []

freq = {}

for num in arr:
    heapq.heappush(h, -num)
    freq[num] = 0

#ans = []
while h:
    num = -heapq.heappop(h)
    if freq[num]>0:
        freq[num] -= 1
        continue
    
    if num in look_up:
        #ans.append(look_up[num])
        print(look_up[num],end=' ')
        freq[look_up[num]] += 1
    else:
        for i in range(2,num):
            if num%i==0:
                print(num,end=' ')
                freq[num//i] += 1
                break