def main():
    _, k = map(int, raw_input().split())
    aa = set(map(int, raw_input().split()))
    mi = min(aa)
    aa = sorted(i - mi for i in aa)
    le = aa[-1] * k + 1
    dp = [k + 1] * le
    dp[0] = 0
    for a in aa:
        if a:
            for i in xrange(a, le):
                x = dp[i - a] + 1
                if dp[i] > x:
                    dp[i] = x
    print ' '.join(map(str, (i for i, x in enumerate(dp, mi * k) if x <= k)))


if __name__ == '__main__':
    main()
