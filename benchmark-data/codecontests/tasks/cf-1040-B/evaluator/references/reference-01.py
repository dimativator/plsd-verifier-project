n,k=map(int,input().split())
if n%(2*k+1)==0:
    print(n//(2*k+1))
    for i in range(k+1,n+1,2*k+1):
        print(i,end=" ")
else:
    if n%(2*k+1)>=k+1:
        print(n//(2*k+1)+1)
        for i in range(k+1,n+1,2*k+1):
            print(i,end=" ")
    else:
        print(n//(2*k+1)+1)
        for i in range(n%(2*k+1),n+1,2*k+1):
            print(i,end=" ")
            
        
        
        