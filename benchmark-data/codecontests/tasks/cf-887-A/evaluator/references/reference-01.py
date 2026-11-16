n=list(input())
m=len(n)
e=0
s=1
if n.count('1')==0:
    s=0
for i in range(0,m):
    if n[i]=='1':
        e=i
        break
k=n[e:]
if s==1:
    if k.count('0')>=6:
        print('yes')
    else:
        print('no')
else:
    print('no')
