n = int(input())
a = [int(x) for x in input().split(" ")]
a.sort()

for i in range(n):
    if i%2 == 0:
        firval = a[i]
        secval = a[i-1]
        if i == 0:
            continue
        elif firval > secval:
            a[i],a[i-1] = a[i-1],a[i]
        elif secval >= firval:
            continue
    elif i%2 != 0:
        firval = a[i]
        secval = a[i-1]
        if firval < secval:
            a[i],a[i-1] = a[i-1],a[i]
        elif secval <= firval:
            continue
final = []
for k in a:
    final.append(str(k))
print(' '.join(final))