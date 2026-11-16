n,k = map(int,input().split())
s = list(map(int,input().split()))
p = list(map(int,input().split()))
r = {}
r2 = []
for i in range(n):
    if s[i] in r:
        if r[s[i]]>p[i]:
            r2.append(p[i])
        else:
            r2.append(r[s[i]])
            r[s[i]] = p[i]
    else:
        r[s[i]] = p[i]
r1 = k-len(r)
#print(r,r2)
print(sum(sorted(r2)[:r1]))

