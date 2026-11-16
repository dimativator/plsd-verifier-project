for i in range(int(input())):
    k=int(input())
    a=list(map(int,input().split()))
    a.sort()
    c,d=0,0
    i=1
    e=0
    for j in range(len(a)):
        if(a[j]%2==0):
            c+=1
        else:
            d+=1
    if(c%2==0 and d%2==0):
        print("YES")
    else:
        c,d=0,0
        while(i<len(a)):
            if(a[i]-a[i-1]==1):
                a.pop(i)
                a.pop(i-1)
                e+=2
                break
            i+=1
        for i in range(len(a)):
            if(a[i]%2==0):
                c+=1
            else:
                d+=1
        if(c%2==0 and d%2==0 and e+len(a)==k):
            print("YES")
        else:
            print("NO")
        
    
            
            