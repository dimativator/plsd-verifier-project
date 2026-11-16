from itertools import product


def main():
    n, s, t = int(input()), input(), input()
    print('YES')
    abc = ('abc', 'acb', 'bac', 'bca', 'cab', 'cba')
    if s[0] != s[1] and t[0] != t[1]:
        for p in abc:
            if s not in p and t not in p:
                print(p[0] * n, p[1] * n, p[2] * n, sep='')
                return
    for pp in product(abc, repeat=min(n, 2)):
        p = f'{pp[0]}{pp[-1]}{pp[0]}'[:min(n, 3) * 3]
        if s not in p and t not in p:
            break
    print((p[:6] * ((n + 1) // 2))[:n * 3])


if __name__ == '__main__':
    main()
