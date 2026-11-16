n = int(input())
fix = list()
factors = set(range(1, n + 1))
for i in map(int, input().split()):
    if i in factors:
        factors.remove(i)
        fix.append(i)
    else:
        fix.append(None)
print(' '.join(str(factors.pop()) if i is None else str(i) for i in fix))