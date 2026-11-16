from bisect import bisect_left as bl
I=10000000
n=int(input())+1
c=[0]*n
for i,x in enumerate(map(int,input().split())): c[x]=i
d = [n-c[int(x)] for x in input().split()]
c=[I]*n
for i in d: c[bl(c,i)]=i
print( c.index(I))