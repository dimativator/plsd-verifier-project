from math import sqrt

n,hn = list(map(int,input().split()))
kn = sqrt(n)
h = hn/kn
for i in range(1,n):
    print(h*sqrt(i),end = ' ')