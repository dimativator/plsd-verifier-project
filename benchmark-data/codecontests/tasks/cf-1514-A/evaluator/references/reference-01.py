import math
rr = input
rri = lambda: int(rr())
rrm = lambda: list(map(int, rr().split()))

def perfect_square(n):
    root = math.sqrt(n)
    if int(root + 0.5) ** 2 == n:
        return True
    else:
        return False

def prod(lst):
    ret = 1
    for i in lst:
        ret *= i
    return ret


def solve():
    n =  rri()
    lst = rrm()
    for i in lst:
        if not perfect_square(i):
            return "YES"
    #for i in range(n):
        #for j in range(i,n):
        #    print(i, j)
         #   if not perfect_square(prod(lst[i:j+1])):
          #      return 'YES'
    return 'NO'

T = rri()


for t in range(T):


    print(solve())