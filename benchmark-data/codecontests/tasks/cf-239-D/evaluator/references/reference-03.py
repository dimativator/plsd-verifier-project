from sys import stdin

rints = lambda: [int(x) for x in stdin.readline().split()]
n, m = rints()
a = rints()
mi = a.index(min(a))

if n == 2:
    print('%d\n%s' % (0, '1 1'))
else:
    a.sort()
    ans = ['1'] * n
    diff1 = (a[-1] + a[-2]) - (a[0] + a[1])
    diff2 = max(a[-1] + a[-2], a[-1] + a[0] + m) - min(a[0] + a[1] + m, a[1] + a[2])
    if diff2 < diff1:
        ans[mi] = '2'

    print('%d\n%s' % (min(diff2, diff1), ' '.join(ans)))
