#not done by myself
t=int(input())
fflg=0
if t==3000: fflg=1
cnt=1
while t!=0:
    
    t-=1
    n=int(input())
    lst=input().split(" ")
   # if fflg==1 and cnt==59: print(lst)
    for i in range(0,n,1):
        lst[i]=int(lst[i])
    flg=0
    mini=1000000000000000
    psum=[0 for i in range(0,n+1,1)]

    for i in range(0,n-1,1):
        mini=min(mini,lst[i])
        if(lst[i+1]<lst[i]):
            x=lst[i]-lst[i+1]
            psum[0]-=x
            psum[i+1]+=x
            
    cnt+=1
    for i in range(1,n+1,1):
        psum[i]+=psum[i-1]
    for i in range(0,n,1):
        if lst[i] + psum[i] <0: flg=1

    if(flg==1): print("NO")
    else: print("YES")