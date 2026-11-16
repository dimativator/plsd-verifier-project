tc = int(input())
while tc > 0:
    n, k = map(int, input().split())
    t = 0
    for i in range(n):
        if t + i >= k:
            s = ["a"] * n
            s[n - i - 1] = "b"
            s[n - k + t] = "b"
            print("".join(s))
            break
        t += i
    tc -= 1