import sys,math,bisect
from random import randint
inf = float('inf')
mod = 998244353
"========================================"
def lcm(a,b):
    return int((a/math.gcd(a,b))*b)
def gcd(a,b):
    return int(math.gcd(a,b))
def tobinary(n):
    return bin(n)[2:]
def binarySearch(a,x):
    i = bisect.bisect_left(a,x)
    if i!=len(a) and a[i]==x:
        return i
    else:
        return -1
def lowerBound(a, x):
    i = bisect.bisect_left(a, x)
    if i:
        return (i-1)
    else:
        return -1
def upperBound(a,x):
    i = bisect.bisect_right(a,x)
    if i!= len(a)+1 and a[i-1]==x:
        return (i-1)
    else:
        return -1
def primesInRange(n):
    ans = []
    prime = [True for i in range(n+1)]
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n+1, p):
                prime[i] = False
        p += 1
    for p in range(2, n+1):
        if prime[p]:
            ans.append(p)
    return ans
def primeFactors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3,int(math.sqrt(n))+1,2):
        while n % i== 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors
def isPrime(n,k=5):
    if (n <2):
        return True
    for i in range(0,k):
        a = randint(1,n-1)
        if(pow(a,n-1,n)!=1):
            return False
    return True
"========================================="
"""
n = int(input())
n,k = map(int,input().split())
arr = list(map(int,input().split()))
"""
from collections import deque,defaultdict,Counter
import heapq,string

n,k = map(int,input().split())
arr = list(map(int,input().split()))
if max(arr)-min(arr)>k:
    print('NO')
else:
    ans = [[0]*i for i in arr]
    c=min(arr)
    k=1
    for i in range(n):
        for j in range(min(arr)):
            ans[i][j]=1
    while c<max(arr):
        for i in range(n):
            if len(ans[i]) > c:
                ans[i][c]=k
        c+=1
        k+=1
    print('YES')
    for i in ans:
        print(*i)
