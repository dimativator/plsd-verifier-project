a,b,c,d=map(int,input().split(" "))
li=[0]*int(pow(10,6)+2)
n=int(pow(10,6)+2)
for i in range(a,b+1):
  li[i+b]+=1
  li[i+c+1]-=1
for i in range(1,n):
  li[i]+=li[i-1]
for i in range(1,n):
  li[i]+=li[i-1]   
ans=0
for i in range(c,d+1):
  ans+=li[n-1]-li[i]
print(ans)


