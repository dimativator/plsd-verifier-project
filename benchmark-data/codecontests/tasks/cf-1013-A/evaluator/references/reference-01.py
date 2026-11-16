n=int(input())
p=input().split(' ')
c=input().split(' ')
t=z=0
for k in range(n):
    t+=int(p[k])
    z+=int(c[k])
if (t<z):
    print('No')
else:
    print('Yes')
