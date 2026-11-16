#!/usr/bin/pypy3

from sys import stdin, stdout
input, print = stdin.readline, stdout.write

p = 0

def readints():
    return list(map(int, input().split()))
def writeln(x):
    print(str(x) + '\n')

def mod(x):
    return (x % p + p) % p
def matmul(a, b):
    n = len(a)
    c = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c[i][j] = (c[i][j] + a[i][k] * b[k][j]) % p
    return c
def matpow(b, p):
    n = len(b)
    res = [[0 if x != y else 1 for x in range(n)] for y in range(n)]
    while p:
        if p & 1:
            res = matmul(res, b)
        b = matmul(b, b)
        p >>= 1
    return res




def main():
    global p
    
    n, x, y, p = readints()
    a = [each % p for each in sorted(readints())]
    if n == 1:
        writeln(a[0])
        return


    """
    [a sum] * [[1 -1],   = [a sum]
            [0 3]]
    [sc mv] * [[0 1],
                [1, 1]] = [mv mv+sc]
    """

    b = matpow([
        [1, -1],
        [0, 3]], x)
    sum0 = matmul([
        [a[0] + a[-1], sum(a)],
        [0, 0]], b)[0][1]

    b = matpow([
        [0, 1],
        [1, 1]], x)
    maxa = matmul(
        [[a[-2], a[-1]],
        [0, 0]], b)[0][1]

    b = matpow([
        [1, -1],
        [0, 3]], y)
    sum1 = matmul([
        [a[0] + maxa, sum0],
        [0, 0]], b)[0][1]

    writeln(mod(sum1))

if __name__ == '__main__':
    main()