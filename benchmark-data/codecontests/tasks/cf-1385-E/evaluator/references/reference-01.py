from sys import stdin, gettrace
from collections import deque

if gettrace():
    inputi = input
else:
    def input():
        return next(stdin)[:-1]


    def inputi():
        return stdin.buffer.readline()


def solve():
    n,m = map(int, inputi().split())
    dadjs = [[] for _ in range(n)]
    dadjd =  [set() for _ in range(n)]
    dedgec = 0
    res = []
    uedge = []
    for _ in range(m):
        t, x, y = map(int, inputi().split())
        if t == 0:
            uedge.append((x-1,y-1))
        else:
            res.append((x-1, y-1))
            dadjs[x-1].append(y-1)
            dadjd[y-1].add(x-1)
            dedgec += 1
    sources = deque(x for x in range(n) if not dadjd[x])
    nlist = []
    while sources:
        s = sources.popleft()
        nlist.append(s)
        for a in dadjs[s]:
            dedgec -= 1
            dadjd[a].remove(s)
            if not dadjd[a]:
                sources.append(a)
        dadjs[s] = []
    if dedgec != 0:
        print("NO")
        return
    npos = [-1] * n
    for i,j in enumerate(nlist):
        npos[j] = i
    for x, y in uedge:
        if npos[x] < npos[y]:
            res.append((x,y))
        else:
            res.append((y,x))
    print("YES")
    for x, y in res:
        print(x+1, y+1)





def main():
    t = int(inputi())
    for _ in range(t):
        solve()


if __name__ == "__main__":
    main()