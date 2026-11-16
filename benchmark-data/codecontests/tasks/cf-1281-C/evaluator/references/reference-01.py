import sys
reader = (s.rstrip() for s in sys.stdin)
input = reader.__next__
MAX=10**9+7
def solve():
    x = int(input())
    s = [int(i) for i in input()]
    ans=len(s)
    c = ""
    l = 0
    while l < x:
        l += 1
        k=len(s)
        if k < x:
            #s += s[l:]*(s[l - 1]-1)
            for i in range(s[l-1] - 1):
                for j in range(l, k):
                        s.append(s[j])

        ans+=  (s[l - 1]-1) *(ans - l)
        ans%=MAX
    print(ans)
t=int(input())
for _ in range(t):
    solve()

#
# mod = 10 ** 9 + 7
#
#
# def solve():
#     x = int(input())
#     s = [int(i) for i in input()]
#     ans = len(s)
#     cur = -1
#     while cur != x - 1:
#         cur += 1
#         if len(s) < x:
#             k = len(s)
#             for _ in range(s[cur] - 1):
#                 for j in range(cur + 1, k):
#                     s.append(s[j])
#         ans += (s[cur] - 1) * (ans - (cur + 1))
#         ans %= mod
#     print(ans)
#
#
# t = int(input())
# for i in range(t):
#     solve()

