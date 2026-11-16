n, k = map(int, input().split())
sp = list(map(int, input().split()))
s = sum(sp) // k
s1 = []
ans, sm = 0, 0
for el in sp:
    sm += el
    ans += 1
    if sm == s:
        s1.append(ans)
        ans, sm = 0, 0
    elif sm > s:
        print("No")
        break
else:
    if sum(s1) == n:
        print("Yes")
        print(*s1)
    else:
        print("No")


