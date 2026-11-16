r = lambda: list(map(int, input().split()))[1:]
n,c = map(int, input().split())

d = []
for _ in range(n):
    for i in r():
        if i<c:
            d.append(str(_+1))
            break
print (len(d))
print (' '.join(d))