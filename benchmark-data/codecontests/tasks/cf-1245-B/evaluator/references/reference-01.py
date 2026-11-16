from math import ceil


t = int(input())
slow = {"S": "R", "R": "P", "P": "S"}
for _ in range(t):
    n = int(input())
    a, b, c = map(int, input().split())
    s = input()
    slow2 = {"S": a, "R": b, "P": c}
    res = 0
    ans = [''] * n
    for i in range(n):
        if slow2[s[i]] > 0:
            res += 1
            ans[i] = slow[s[i]]
            slow2[s[i]] -= 1
    if res >= ceil(n / 2):
        for i in range(n):
            if ans[i] == '':
                if slow2[s[i]] > 0:
                    ans[i] = slow[s[i]]
                    slow2[s[i]] -= 1
                elif slow2[slow[s[i]]] > 0:
                    ans[i] = slow[slow[s[i]]]
                    slow2[slow[s[i]]] -= 1
                else:
                    slow2[slow[slow[s[i]]]] -= 1
                    ans[i] = slow[slow[slow[s[i]]]]
        print("YES")
        print(''.join(ans))
    else:
        print("NO")
