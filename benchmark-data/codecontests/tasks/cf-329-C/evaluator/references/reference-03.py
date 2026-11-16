from sys import stdin
from collections import defaultdict
from time import time
from random import shuffle
def main():
    st = time()
    n, m = map(int, stdin.readline().split())
    d = defaultdict(set)
    for i in xrange(m):
        a, b = map(int, stdin.readline().split())
        d[a].add(b)
        d[b].add(a)
    c = range(1, n+1)
    while time() - st < 2.8:
        shuffle(c)
        bad = 0
        for i in xrange(m):
            if c[-i] in d[c[-i-1]]:
                bad = 1
                break
        if bad: continue
        for i in xrange(m):
            print c[-i], c[-i-1]
        return
    print -1
main()
