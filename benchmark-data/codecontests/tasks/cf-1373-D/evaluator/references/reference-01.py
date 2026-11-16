import sys,random
input=sys.stdin.readline
T=int(input())

for _ in range(T):
    n=int(input())
    A=list(map(int,input().split()))

    '''n=random.randint(1,10)
    A=[]
    
    for i in range(n):
        A.append(random.randint(1,10))

    print(n)
    print(*A)'''
    B=[]
    C=[]
    for i in range(0,n,2):
        if (i<n-1):
            B.append(A[i+1]-A[i])

    for i in range(1,n,2):
        if (i<n-1):
            C.append(A[i]-A[i+1])


    ans,mv,maxv=[0,n-1],0,0
    l,r=0,1
    for i in range(len(B)):
        mv=mv+B[i]

        if (mv>maxv):
            r=(i*2)+1
            ans=[l,r]
            maxv=mv

        if (mv<=0):
            l=(i*2)+2
            mv=0

    
    mv=0
    l,r=1,2
    for i in range(len(C)):
        mv=mv+C[i]
        if(mv>maxv):
            r=(i*2)+2
            ans=[l,r]
            maxv=mv

        if (mv<=0):
            l=((i+1)*2)+1
            mv=0
 
    l,r=ans[0],ans[1]
    ans=0

    for i in range(0,min(l,n),2):
        ans=ans+A[i]

    for i in range(l,min(r+1,n)):
        if(i%2!=0):
            ans=ans+A[i]

    for i in range(r+1,n):
        if(i%2==0):
            ans=ans+A[i]

    v=0
    for i in range(0,n,2):
        v=v+A[i]
    ans=max(ans,v)
    print(ans)
        
