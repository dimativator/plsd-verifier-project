n, k = [int(x) for x in input().strip().split()]
S = input().strip()

if n == 1 and k == 1:
    res = '0'
elif k == 0:
    res = S
else:
    S = [c for c in S]

    if S[0] != '1':
        S[0] = '1'
        k -= 1

    i = 1
    while k > 0:
        if i >= n:
            break
        if S[i] == '0':
            i += 1
            continue

        S[i] = '0'
        k -= 1
        i += 1

    res = "".join(S)

print(res)
