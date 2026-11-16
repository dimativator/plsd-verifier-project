"""#N=int(input())
n,k=map(int,input().split())
s=input()
L=[0]*26
#s=[int(x) for x in input().split()]
for j in range(0,len(s)):
    L[ord(s[j])-65]=L[ord(s[j])-65]+1
ans=1000000007
for j in range(0,k):
    ans=min(ans,L[j])
ans=k*ans
print(ans)"""
import math
pre=[]
for i in range(0,45010):
    pre.append(((i*(i+1))//2))
#print(pre[:100])
n=int(input())
if(n==0 or n==1 or n==2):
    print('No')
else:
    temp=0
    t=pre[n]
    pos=-1
    for j in range(1,n+1):
        if(math.gcd(pre[j],t-pre[j])>1):
            temp=1
            pos=j
            break
    if(temp==0):
        print('No')
    else:
        print('Yes')
        print(pos,end=" ")
        for j in range(1,pos+1):
            print(j,end=" ")
        print(" ")
        print(n-j,end=" ")
        for j in range(pos+1,n+1):
            print(j,end=" ")
        print(" ")
