import sys
def input():
    str = sys.stdin.readline()
    return str[:-1]
def unique(x, first, last):
    if first == last:
        return last
    result = first
    while first + 1 != last:
        first += 1
        if(x[result] != x[first]):
            result += 1
            x[result] = x[first]
    return result + 1
 
 
q = int(input())
for _ in range(q):
    n, r = map(int, input().split())
    x = list(map(int, input().split()))
    x.sort(reverse=True)
    siz = unique(x, 0, len(x))
    rc = 0
    tt = 0
    for i in range(siz):
        a = x[i]
        if rc < a:
            rc += r
            tt += 1
        else:
            break
    print(tt)