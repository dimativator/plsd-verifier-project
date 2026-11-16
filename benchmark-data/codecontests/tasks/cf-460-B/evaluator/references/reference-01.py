a,b,c=map(int,input().split())
L=[]
for i in range(1,82):
    val=b*(i**a)+c
    check=0
    if val>0 and val<10**9:
        s=str(val)
        for j in s:
            check+=int(j)
        if check==i:
            L.append(val)
if len(L)==0:
    print(0)
else:
    print(len(L))
    print(*L)