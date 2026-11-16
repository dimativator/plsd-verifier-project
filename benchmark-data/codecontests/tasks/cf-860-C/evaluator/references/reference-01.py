import math,string,itertools,fractions,heapq,collections,re,array,bisect,sys,random,time,copy,functools

sys.setrecursionlimit(10**7)
inf = 10**20
eps = 1.0 / 10**10
mod = 10**9+7

def LI(): return [int(x) for x in sys.stdin.readline().split()]
def LI_(): return [int(x)-1 for x in sys.stdin.readline().split()]
def LF(): return [float(x) for x in sys.stdin.readline().split()]
def LS(): return sys.stdin.readline().split()
def I(): return int(sys.stdin.readline())
def F(): return float(sys.stdin.readline())
def S(): return input()


def main():
    n = I()
    a = set()
    b = set()
    for _ in range(n):
        f,t = LS()
        if t == '0':
            b.add(f)
        else:
            a.add(f)
    al = len(a)
    bl = len(b)
    r = []
    ta = set([str(i) for i in range(1,al+1)])
    tb = set([str(i) for i in range(al+1,al+bl+1)])
    bb = tb & b
    b -= bb
    tb -= bb
    aa = ta & a
    a -= aa
    ta -= aa

    ua = a & tb
    ub = b & ta
    sa = ta - b
    sb = tb - a
    ran = 'iehn00'
    while ua or ub:
        if not sa and not sb:
            if ua:
                t = ua.pop()
                sb.add(t)
                a.remove(t)
                a.add(ran)
            else:
                t = ub.pop()
                sa.add(t)
                b.remove(t)
                b.add(ran)
            r.append('move {} {}'.format(t, ran))
        if sa:
            t = sa.pop()
            if ua:
                k = ua.pop()
                a.remove(k)
                sb.add(k)
            else:
                k = a.pop()
            ta.remove(t)
            r.append('move {} {}'.format(k, t))
        if sb:
            t = sb.pop()
            if ub:
                k = ub.pop()
                b.remove(k)
                sa.add(k)
            else:
                k = b.pop()
            tb.remove(t)
            r.append('move {} {}'.format(k, t))

    while a:
        k = a.pop()
        t = ta.pop()
        r.append('move {} {}'.format(k, t))

    while b:
        k = b.pop()
        t = tb.pop()
        r.append('move {} {}'.format(k, t))

    return '{}\n'.format(len(r)) + '\n'.join(r)




print(main())








# Made By Mostafa_Khaled