def run():
    n = int(input())
    a = [int(x) for x in input().split()]

    _s = set(a)
    if len(_s) == 1:
        print('No')
        return
    if len(_s) == 2:
        print('Yes')
        return


    def check(dy, base):
        st = [False] * n
        for i in range(n):
            if (a[i] - a[base]) * 2 == dy * (i - base):
                st[i] = True

        for i, s in enumerate(st):
            if not s:
                newbase = i
                break
        else:
            return False

        base = newbase
        for i in range(n):
            if (a[i] - a[base]) * 2 == dy * (i - base):
                st[i] = True

        return not (False in st)

    if check((a[1]-a[0])*2, 0) or check((a[2]-a[1])*2, 1) or check((a[2]-a[0]), 0):
        print('Yes')
    else:
        print('No')

run()
