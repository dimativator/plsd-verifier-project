p,q,l,r=list(map(int,input().split()))
a=[]
for i in range(p):
    k,j=list(map(int,input().split()))
    a.append((k,j))
b=[]
for i in range(q):
    k,j=list(map(int,input().split()))
    b.append((k,j))
b.sort(key=lambda h:h[0])
count=0
for i in range(l,r+1):
    for j in range(len(b)):
        gg=0
        for k in range(len(a)):
            if b[j][0]+i<=a[k][0]<= a[k][1]<=b[j][1]+i or a[k][0]<=b[j][0]+i<=a[k][1]<=b[j][1]+i or b[j][0]+i<=a[k][0]<=b[j][1]+i<=a[k][1] or a[k][0]<=b[j][0]+i<=b[j][1]+i<=a[k][1]:
                count+=1
                gg=1
                break
        if gg==1:
            break
print(count)
            
        



