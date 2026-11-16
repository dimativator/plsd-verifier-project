n=int(input());k=0
if n==1:print(0);exit()
a=list(map(int,input().split()));b=[];c=[]
for i in range(n*n):b.append(0)
for i in range(n):
    if b[a[i]]==0:b[a[i]]=a[i]
    else:c.append(a[i])
for i in range(len(c)):
    for j in range(c[i],len(b)):
        if b[j]==0:k+=b[j-1]-c[i]+1;b[j]=j;break
print(k)