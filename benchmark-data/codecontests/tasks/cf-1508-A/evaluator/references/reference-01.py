import itertools

def solve(a, b):
    if a.count("1") * 2 >= len(a) and b.count("1") * 2 >= len(b):
        ch = "1"
        other = "0"
    else:
        ch = "0"
        other = "1"
    res = []
    i = 0
    j = 0
    ilast = -1
    jlast = -1
    while i < len(a) and j < len(b):
        while i < len(a) and a[i] != ch:
            i += 1
        while j < len(b) and b[j] != ch:
            j += 1
        res.append(other *  max(i - ilast - 1, j - jlast - 1))

        if i != len(a) or j != len(b):
            res.append(ch)

        ilast = i
        jlast = j
        i += 1
        j += 1

    while i < len(a):
        res.append(a[i])
        i += 1
    while j < len(b):
        res.append(b[j])
        j += 1
    return ''.join(res)
            


for _ in range(int(input())):
    n = int(input())
    a = input()
    b = input()
    c = input()
    na1 = a.count("1")
    nb1 = b.count("1")
    nc1 = c.count("1")
    res = None

    if na1 >= n and nb1 >= n or na1 <= n and nb1 <= n:
        res = solve(a, b)
    elif na1 >= n and nc1 >= n or na1 <= n and nc1 <= n:
        res = solve(a, c)
    elif nb1 >= n and nc1 >= n or nb1 <= n and nc1 <= n:
        res = solve(b, c)
    else:
        raise RuntimeError("unexpected")
    print(res)




