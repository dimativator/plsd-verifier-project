a = [list(map(int, input().split(" "))) for x in range(int(input()))]
pl = []; ol = []
for i in range(len(a)):
    if a[i][0] < 0:
        ol.append(a[i])
    else:
        pl.append(a[i])
pl.sort(); ol.sort(); ol.reverse()
del a; dl = abs(len(ol)-len(pl)); sum = int(0); j = 0
m = min(len(ol), len(pl))
if (len(pl) == 0)and(len(ol) != 0):
    sum = ol[0][1]
    print(sum)
    exit()
elif (len(pl) == 0)and(len(ol) == 0):
    print(sum)
    exit()
elif (len(ol) == 0)and(len(pl) != 0):
    sum = pl[0][1]
    print(sum)
    exit()
elif dl > 1:
    for i in range(m):
        sum = sum + pl[i][1]+ ol[i][1]
        j = i
    if len(pl)>len(ol):
        sum = sum+pl[j+1][1]
    else:
        sum = sum+ol[j+1][1]
    print(sum)
    exit()
elif dl == 0 or dl == 1:
    for i in range(len(pl)):
        sum = sum + pl[i][1]
    for i in range(len(ol)):
        sum = sum + ol[i][1]        
    print(sum)
    exit()
    
        
        





    
    
