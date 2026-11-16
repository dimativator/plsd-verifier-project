import sys


def main():
    n, w, h = map(int, sys.stdin.readline().split())
    gv = {}
    gh = {}
    for i in range(n):
        g, p, t = map(int, sys.stdin.readline().split())
        c = p - t
        t = (g, p, -t, i)
        if g == 1:
            if c in gv:
                gv[c].append(t)
            else:
                gv[c] = [t]
        else:
            if c in gh:
                gh[c].append(t)
            else:
                gh[c] = [t]

    a = [0] * n
    u = {}
    for k in gv:
        g = gv[k]
        u[k] = True
        if k in gh:
            g = sorted(g, key=lambda x: x[1])
            g2 = sorted(gh[k], key=lambda x: x[1], reverse=True)
            l1 = len(g)
            l2 = len(g2)
            q = [(j[1], h) for j in g] + [(w, j[1]) for j in g2]
            for i in range(l2):
                a[g2[i][3]] = q[i]
            for i in range(l2, l2 + l1):
                a[g[i - l2][3]] = q[i]
        else:
            for i in g:
                a[i[3]] = (i[1], h)
    for k in gh:
        if k not in u:
            for i in gh[k]:
                a[i[3]] = (w, i[1])
    for i in range(n):
        print(a[i][0], a[i][1])


main()
