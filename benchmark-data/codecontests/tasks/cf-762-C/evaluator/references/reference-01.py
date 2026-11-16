from sys import stdin


def main():
    t = stdin.readline()
    s = stdin.readline()
    n = len(s) - 1
    m = len(t) - 1
    post = [-1] * n
    ss = n - 1
    st = m - 1
    while st >= 0 and ss >= 0:
        if t[st] == s[ss]:
            post[ss] = st
            ss -= 1
        st -= 1
    pre = [-1] * n
    ss = 0
    st = 0
    while st < m and ss < n:
        if t[st] == s[ss]:
            pre[ss] = st
            ss += 1
        st += 1
    low = 0
    high = n
    min_ans = n
    start = -1
    end = -1
    while low < high:
        mid = (low + high) >> 1
        ok = False
        if post[mid] != -1:
            if mid < min_ans:
                min_ans = mid
                start = 0
                end = mid - 1
                ok = True
        for i in range(1, n - mid):
            if pre[i - 1] != -1 and post[i + mid] != -1 and post[i + mid] > pre[i - 1]:
                if mid < min_ans:
                    min_ans = mid
                    start = i
                    end = i + mid - 1
                    ok = True
        if pre[n - mid - 1] != -1:
            if mid < min_ans:
                min_ans = mid
                start = n - mid
                end = n - 1
                ok = True
        if not ok:
            low = mid + 1
        else:
            high = mid
    ans = []
    for i in range(n):
        if start <= i <= end:
            continue
        ans.append(s[i])
    if min_ans == n:
        print('-')
    else:
        print(''.join(ans))


if __name__ == '__main__':
    main()
