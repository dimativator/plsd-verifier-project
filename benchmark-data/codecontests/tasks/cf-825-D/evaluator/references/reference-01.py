from collections import Counter
import sys
input = sys.stdin.readline

s = list(input().rstrip())
t = input().rstrip()
cnt1 = Counter(s)
cnt2 = Counter(t)

if cnt1['?'] == 0:
    print(*s, sep='')
    exit()

ok, ng = 0, 10**9
while abs(ok - ng) > 1:
    mid = (ok + ng) // 2
    hatena = cnt1['?']
    for k, v in cnt2.items():
        hatena -= max(0, v*mid - cnt1[k])

    if hatena >= 0:
        ok = mid
    else:
        ng = mid

keys = list(cnt2.keys())

for i in range(len(s)):
    if s[i] == '?':
        while keys and cnt2[keys[-1]] * ok <= cnt1[keys[-1]]:
            keys.pop()
        if keys:
            s[i] = keys[-1]
            cnt1[keys[-1]] += 1
        else:
            s[i] = 'z'

print(*s, sep='')
