import sys
sys.stderr = sys.stdout


def hood(n, k, C):
    C.sort()
    m, r = divmod(sum(C), n)
    m1 = (m + 1) if r else m

    c_lo = C[0]
    k_lo = k
    for i, c in enumerate(C):
        if c_lo == m:
            break
        c_m = min(c, m)
        dc = c_m - c_lo
        dk = i * dc
        if k_lo >= dk:
            k_lo -= dk
            c_lo = c_m
        else:
            dc = k_lo // i
            c_lo += dc
            break

    c_hi = C[-1]
    k_hi = k
    for i, c in enumerate(reversed(C)):
        if c_hi == m1:
            break
        c_m1 = max(c, m1)
        dc = c_hi - c_m1
        dk = i * dc
        if k_hi >= dk:
            k_hi -= dk
            c_hi = c_m1
        else:
            dc = k_hi // i
            c_hi -= dc
            break

    return c_hi - c_lo


def main():
    n, k = readinti()
    C = readintl()
    print(hood(n, k, C))

##########

def readint():
    return int(input())


def readinti():
   return map(int, input().split())


def readintt():
   return tuple(readinti())


def readintl():
   return list(readinti())


def readinttl(k):
    return [readintt() for _ in range(k)]


def readintll(k):
    return [readintl() for _ in range(k)]


def log(*args, **kwargs):
    print(*args, **kwargs, file=sys.__stderr__)


if __name__ == '__main__':
    main()
