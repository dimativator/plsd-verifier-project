n, k1, k2 = map(int, input().split())
a1 = list(map(int, input().split()))
a2 = list(map(int, input().split()))

e = []
for i in range(n):
    e.append(abs(a1[i]-a2[i]))
#print(e)

for k in range(k1+k2):
    e[e.index(max(e))] = abs(max(e) - 1)

print(sum(i * i for i in e))