import math
for i in range(int(input())):
    n=int(input())
    a=100-n
    b=n
    if n==100:
        print(1)
    else:
        g=math.gcd(a,b)
        print(a//g+b//g)
