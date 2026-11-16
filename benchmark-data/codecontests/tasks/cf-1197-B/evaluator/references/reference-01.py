n=int(input())
ar=list(map(int,input().split()))
m=max(ar)
ind=-1
for i in range(n):
    if(ar[i]==m):
        ind=i
ans="YES"
a1=[]
a2=[]
for i in range(ind):
    a1.append(ar[i])
    a2.append(ar[i])
a2.sort()

for i in range(ind):
    if(a1[i]!=a2[i]):
        ans="NO"

a3=[]
a4=[]
for i in range(ind+1,n):
    a3.append(ar[i])
    a4.append(ar[i])

a4.sort(reverse=True)
for i in range(len(a3)):
    if(a3[i]!=a4[i]):
        ans="NO"

print(ans)