n, h, k = map(int, input().split())
pots = map(int, input().split())

comb = [0]
for pot in pots:   
    if (comb[-1] % k + pot <= h):
        comb[-1] += pot
    else:
        comb.append(pot)

sec = lambda x : x // k + int(x % k > 0)
ans = sum(map(sec, comb))
print(ans)