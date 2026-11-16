import os
from io import BytesIO, StringIO
#input = BytesIO(os.read(0, os.fstat(0).st_size)).readline
from collections import defaultdict

def input_as_list():
    return list(map(int, input().split()))

def array_of(f, *dim):
    return [array_of(f, *dim[1:]) for _ in range(dim[0])] if dim else f()

def main():
    n = int(input())
    a = input_as_list()

    out = array_of(int, n, n)

    def put(x, i, j):
        out[i][j] = x
        out[n-i-1][j] = x
        out[i][n-j-1] = x
        out[n-i-1][n-j-1] = x

    d = defaultdict(int)
    for x in a:
        d[x] += 1

    if n%2 == 0:
        for v in d.values():
            if v%4 != 0:
                print('NO')
                return
        ix = 0
        for k in d.keys():
            for _ in range(d[k]//4):
                i, j = divmod(ix, n//2)
                put(k, i, j)
                ix += 1
    else:
        ones = []
        twos = []
        fours = []

        for k, v in d.items():
            if v%2 != 0:
                if ones:
                    print('NO')
                    return
                else:
                    ones.append(k)
                    d[k] -= 1

        for k, v in d.items():
            if v%4 != 0:
                if len(twos) >= n:
                    print('NO')
                    return
                else:
                    twos.append(k)
                    d[k] -= 2

        for k, v in d.items():
            if v%4 != 0:
                print('NO')
                return
            else:
                for _ in range(v//4):
                    fours.append(k)

        if not ones:
            print('NO')
            return

        while len(twos) < n-1:
            k = fours.pop()
            twos.append(k)
            twos.append(k)

        ix = 0
        for k in fours:
            i, j = divmod(ix, n//2)
            put(k, i, j)
            ix += 1

        for i in range(n//2):
            k = twos.pop()
            put(k, i, n//2)

        for i in range(n//2):
            k = twos.pop()
            put(k, n//2, i)

        put(ones[0], n//2, n//2)


    out_str = ['YES\n']
    for i in range(n):
        for j in range(n):
            out_str.append(str(out[i][j]) + ' ')
        out_str.append('\n')
    print(''.join(out_str))


main()