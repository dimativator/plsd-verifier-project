n,m,d=map(int,input().split())
x=[]
y=[]
for i in range(n):
    a=list(map(int,input().split()))
    y+=a
    x.append(a)
y.sort()
e=y[(0+n*m-1)//2]
a=x[0][0]%d
count=0
ans=0
for i in x:
    for j in range(len(i)):
        if(i[j]%d!=a):
            pass
        else:
            count+=1
            ans+=(max(i[j],e)-min(i[j],e))//d         
if(count==n*m):
    print(ans)
else:
    print(-1)