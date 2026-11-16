s=input()
a=s.count('m')
f=True
ans=0
if(a>0):
    f=False
a=s.count('w')
if(a>0):
    f=False
n=len(s)    
if(f==True):
    dp=[0]*(n+1)
    dp[0]=1
    dp[1]=1
    for i in range(2,n+1):
        if(s[i-1]==s[i-2] and (s[i-1]=='u' or s[i-1]=='n')):
           dp[i]=(dp[i-1]+dp[i-2])%1000000007
        else:
            dp[i]=dp[i-1]
    print(dp[n])
else:
    print(0)
    