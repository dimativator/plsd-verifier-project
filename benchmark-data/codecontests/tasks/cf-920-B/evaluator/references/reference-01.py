if __name__ == '__main__':
    cin = input
    t = int(cin())

    while t > 0:
        n = int(cin())
        a, cnt = [0] * n, 0
        for i in range(n):
            l, r = map(int, cin().split())
            if r >= cnt + max(l - cnt, 1):
                cnt += max(l - cnt, 1)
                a[i] += cnt
        print(*a)
        t -= 1