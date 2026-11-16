n=int(input())
s=list(map(int,input().split()))
m,h,d=0,0,0
for i in range(n):
    m+=h-s[i]
    if(m<0):
        d-=m
        m=0
    h=s[i]
print(d)