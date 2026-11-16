import sys,os,io
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline
input = sys.stdin.readline
from collections import defaultdict
from math import gcd

 
for _ in range (int(input())):
    n,m = [int(i) for i in input().split()]
    mod = 10**9 + 7
    a = []
    cnt = 0
    for i in range (n):
        si = list(input().strip())
        cnt += si.count('#')
        a.append(si)
    temp = 0
    if cnt==m*n:
        temp+=1
    print(pow(2,cnt,mod)-temp)