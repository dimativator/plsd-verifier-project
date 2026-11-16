import math
n=int(input())
d=n//2
c=n-d
while math.gcd(c,d)!=1:
    c+=1
    d-=1
print(d,c)
        