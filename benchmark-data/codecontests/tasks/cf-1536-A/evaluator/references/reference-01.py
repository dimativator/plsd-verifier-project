from sys import stdin
input = stdin.readline

def solve():
    n = int(input())
    a = [int(x) for x in input().split()]
    for i in a:
        if i < 0:
            print("NO")
            return
    ans = list(range(0, 101))
    print("YES")
    print(len(ans))
    print(*ans)

t = int(input())
for _ in range(t):
    solve()