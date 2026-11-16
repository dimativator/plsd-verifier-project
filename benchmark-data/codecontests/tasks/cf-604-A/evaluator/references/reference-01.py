t=list(map(int,input().split()))
w=list(map(int,input().split()))
q,z=map(int,input().split())
c=0
v=0
for i in range(500,3000,500):
  x=(1-(t[v]/250))*i-50*w[v]
  a=max(0.3*i,x)
  c=c+a
  v=v+1
f=q*100-z*50
dp=c+f
print(int(dp))
