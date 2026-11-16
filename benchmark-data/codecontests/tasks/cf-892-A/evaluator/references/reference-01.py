import sys
sys.setrecursionlimit(100000000)
# def input(): return sys.stdin.readline()[:-1]
def iin(): return int(input())
def impin(): return map(int, input().split())
def irrin(): return [int(x) for x in input().split()]
def imrin(n): return [int(input()) for _ in range(n)]


n = iin()
arr = irrin()
brr = irrin()
brr.sort(reverse=True)
if sum(arr)<=brr[0]+brr[1]:
    print("YES")
else:
    print('NO')
