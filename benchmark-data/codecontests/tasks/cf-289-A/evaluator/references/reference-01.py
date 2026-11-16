a,b  = map(int, input().split())
c = 0

for i in range(a):
    d,e = map(int, input().split())
    c += (e-d+1)

if not(c%b):
    print(0)
else:
    print((b-(c%b))%b)