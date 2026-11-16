def gcd(x,y):
    if x % y == 0:
        return y
    else:
        return gcd(y,x%y)

def bezout(x,y):
    if x % y == 0:
        return (0,1)
    else:
        t,s = bezout (y,x%y)
        return (s,t-(x//y)*s)
        
a,b,c = map(int,input().split())
if a == 0:
    if c % b == 0:
        print("%d %d" % (0,-c//b))
    else:
        print(-1)
    exit()
if b == 0:
    if c % a == 0:
        print("%d %d" % (-c//a,0))
    else:
        print(-1)
    exit()
if c % gcd(a,b) != 0:
    print(-1)
else:
    x,y = bezout(a,b)
    m = -c//gcd(a,b)
    print("%d %d" % (m*x,m*y))