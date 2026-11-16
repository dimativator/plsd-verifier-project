n=int(input())
a,b,r=1,2,''
for i in range(1,n+1):
  if i==a: r+='O';a,b=b,a+b
  else: r+='o'
print(r)