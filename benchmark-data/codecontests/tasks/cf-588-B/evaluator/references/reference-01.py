import math
#n,k = map(int, input().strip().split(' '))
n=int(input())
#lst = list(map(int, input().strip().split(' ')))
if n==1 or n==2 or n==3:
    print(n)
else:
    p=math.sqrt(n)
    l=[1,n]
    c=1
    for j in range(2,int(p)+1):
        if n%j==0:
            l.insert(c,j)
            if n//j!=j:
                l.insert(c+1,n//j)
            c+=1
            while(True):
                if l[-1]%(j*j)==0:
                    del l[-1]
                else:
                    break
    i1=1
    i2=-1
    
    while(i1<len(l)):
        if l[i1]==l[-1]:
            break
        else:
            if l[i2]%l[i1]**2==0:
                del l[i2]
            else:
                if l[i2]<l[i1]**2:
                    i1+=1
                    i2=-1
                else:
                    i2-=1

                
    print(l[-1])
        
            
            
            