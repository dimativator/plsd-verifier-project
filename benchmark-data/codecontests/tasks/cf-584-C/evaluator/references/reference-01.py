fs = frozenset(list("abc"))

def calc(s1, s2):
    return len(list(filter(lambda x: x[0] == x[1], zip(s1, s2))))

if __name__ == '__main__':
    n, t = map(int, input().split())
    s1 = input()
    s2 = input()

    q = n - t
    c = calc(s1, s2)
    need = q - c
    w = 0

    ss = ['x'] * len(s1)

    if n - c >= 2 * need:
        for i in range(len(s1)):
            ss[i] = list(fs - frozenset(s1[i]) - frozenset(s2[i]))[0]
            if s1[i] == s2[i]:
                ss[i] = s1[i]

            if s1[i] == s2[i] and need < 0 and w > need:
                w -= 1
                ss[i] = list(fs - frozenset(s1[i]) - frozenset(s2[i]))[0]

            if s1[i] != s2[i] and need > 0 and w < 2 * need:
                if w >= need:
                    ss[i] = s2[i]
                else:
                    ss[i] = s1[i]

                w += 1

        print(''.join(ss))
    else:
        print('-1')