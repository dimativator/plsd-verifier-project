a = str(input())
b = str(input())

k = {'monday':1,'tuesday':2,'wednesday':3,'thursday':4,'friday':5,'saturday':6,'sunday':7}

a=k[a]-1
b=k[b]-1

res = False
res = res or ((a+2)%7+1)%7==b
res = res or ((a+1)%7+1)%7==b
res = res or ((a+6)%7+1)%7==b
if res:
    print("YES")
else:
    print("NO")
