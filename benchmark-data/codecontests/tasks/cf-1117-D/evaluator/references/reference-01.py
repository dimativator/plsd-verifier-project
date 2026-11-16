import sys

MOD = 10**9+7

def mult(A,B):
    n = len(A)
    C = []
    for x in range(n):
        c = [0]*n
        for z in range(n):
            b = B[x][z]
            a = A[z]
            for y in range(n):
                c[y] += a[y]*b
        for y in range(n):
            c[y]%=MOD
        C.append(c)
    return C

def vecmult(A,B):
    n = len(A)
    C = [0]*n
    for z in range(n):
        b = B[z]
        a = A[z]
        for y in range(n):
            C[y] += a[y]*b
    for y in range(n):
        C[y]%=MOD
    return C

n,m = [int(x) for x in input().split()]


#def DP(n):
#    if n<=0:
#        return 1 if n==0 else 0
#    else:
#        return DP(n-m) + DP(n-1)


mapper = [[0]*m for _ in range(m)]

mapper[0][0] = 1
mapper[-1][0] = 1
for i in range(m-1):
    mapper[i][i+1] = 1

def power(A,B,m):
    n = len(A)
    if m == 0:
        return B
    while m>8:
        if m%2==1:
            B = vecmult(A,B)
        A = mult(A,A)
        m//=2
    while m>0:
        B = vecmult(A,B)
        m-=1
    return B
    #return vecmult(A,B)

vec = [1]*m
vec = power(mapper,vec,n)
print(vec[-1]%MOD)