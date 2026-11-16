n = int(input())
north = -100000000
south = 100000000
east = -100000000
west = 100000000
ne = -200000000
nw = -200000000
se = -200000000
sw = -200000000
for i in range(n):
    x,y = map(int,input().split())
    north = max(north,y)
    east = max(east,x)
    south = min(south,y)
    west = min(west,x)
    ne = max(ne,x+y)
    nw = max(nw,y-x)
    se = max(se,x-y)
    sw = max(sw,-1*x-y)
best = 2*(ne-south-west)
best = max(best,2*(nw-south+east))
best = max(best,2*(se+north-west))
best = max(best,2*(sw+north+east))
ans = str(best)
peri = 2*(north-south+east-west)
ans += (" "+str(peri))*(n-3)
print(ans)
