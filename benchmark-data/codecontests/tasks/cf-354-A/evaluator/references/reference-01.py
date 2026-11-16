import sys




n,L,r,QL,QR=map(int,sys.stdin.readline().split())


W=list(map(int,sys.stdin.readline().split()))

minn=10**10
SumsL=[0]*n
SumsR=[0]*n

s=0
for i in range(n):
    s+=W[i]
    SumsL[i]=s

for i in range(n-1):
    ans=L*SumsL[i]+r*(s-SumsL[i])
    if(n-(i+1)>i+1):
        ans+=(abs(n-(i+1)-(i+1))-1)*QR
    elif(i+1>n-(i+1)):
        ans+=(abs(n-(i+1)-(i+1))-1)*QL
    if(ans<minn):
        minn=ans
if(s*L+(QL*(n-1)) < minn):
    minn=s*L+(QL*(n-1))
if(s*r+(QR*(n-1)) < minn):
    minn=s*r+(QR*(n-1))



print(minn)
