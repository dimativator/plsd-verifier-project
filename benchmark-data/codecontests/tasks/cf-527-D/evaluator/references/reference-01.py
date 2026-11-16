def main():
    from bisect import bisect_right as br
    n = int(input())
    ab = [list(map(int, input().split())) for _ in [0]*n]
    ab.sort()

    ans = [-10**20]
    l = 1

    for a, b in ab:
        c = br(ans, a-b)
        d = a+b
        if c == br(ans, d):
            if c == l:
                ans.append(d)
                l += 1
            else:
                ans[c] = d
    print(len(ans)-1)


main()