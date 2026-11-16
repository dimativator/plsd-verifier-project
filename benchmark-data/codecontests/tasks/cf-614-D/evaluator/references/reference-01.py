import bisect as bs
import heapq as hq


def force(cf, cm, f, m):
    return f*cf + m*cm


# def perfect(sa, amax, m):
#     p = 0
#     while sa[-p-1] == amax:
#         p += 1
#     while sa[p] + m >= amax:
#         for _ in range(amax-sa[-p-1]):
#             yield p
#         m -= amax-sa[-p-1]
#         p += 1
#     for _ in range(m+1):
#         yield p
# 
# 
# def improve(sa, amax, m):
#     am = sa[0]
#     i = 1
#     while i < len(a) and sa[i] == am:
#         i += 1
#     while i <= m:
#         for _ in range(i):
#             yield am
#         am += 1
#         m -= i
#         while i < len(a) and sa[i] == am:
#             i += 1
#     for _ in range(m+1):
#         yield am

def mtable(sa):
    mt = [0]*len(sa)
    for i in range(1, len(sa)):
        mt[i] = mt[i-1] + i*(sa[i]-sa[i-1])
    return mt


def maxm(sa, mt, f, k):
    i = bs.bisect_right(mt, k, hi=len(sa)-f)
    return sa[i-1] + (k-mt[i-1])//i


def optimize(a, amax, cf, cm, k):
    if sum(a) + k >= len(a)*amax:
        return len(a)*cf + amax*cm, len(a), amax

    sa = sorted(a)
    f = 0
    while sa[-f-1] == amax:
        f += 1
    mt = mtable(sa)

    of = f
    om = maxm(sa, mt, f, k)
    o = force(cf, cm, of, om)

    while k >= amax - sa[-f-1]:
        k -= amax - sa[-f-1]
        f += 1
        m = maxm(sa, mt, f, k)
        t = force(cf, cm, f, m)
        if t > o:
            of, om, o = f, m, t

    return o, of, om

#     sa = sorted(a)
#     fs = list(perfect(sa, amax, m))
#     ms = list(improve(sa, amax, m))
#     of, om = max(zip(fs, reversed(ms)), key=lambda fm: force(fm[0], fm[1]))
#     return force(of, om), of, om 


def apply(a, amax, of, om):
    # Ensure all values are at least om
    a_ = [max(om, ai) for ai in a]

    # Increase top p values to amax
    h = [(-a[i], i) for i in range(len(a))]
    hq.heapify(h)
    for _ in range(of):
        _, i = hq.heappop(h)
        a_[i] = amax

    return a_


def best_force(a, amax, cf, cm, m):
    t, of, om = optimize(a, amax, cf, cm, m)
    if of == len(a):
        return t, [amax]*len(a)
    else:
        return t, apply(a, amax, of, om)
    


if __name__ == '__main__':
    n, amax, cf, cm, k = map(int, input().split())
    a = list(map(int, input().split()))
    assert len(a) == n
    t, o = best_force(a, amax, cf, cm, k)
    print(t)
    print(' '.join(map(str, o)))
