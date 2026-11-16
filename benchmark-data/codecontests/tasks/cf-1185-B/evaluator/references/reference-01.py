def f():
    a=input()
    i=0
    p=a[i]
    l=[]
    while(i<len(a)):
        temp=1
        t=[p]
        i+=1
        while(i<len(a)):
            if a[i]!=p:
                p=a[i]
                break
            p=a[i]
            t.append(p)
            i+=1
            if i==len(a):
                temp=0
                break
        l.append(t)
        if temp==0:
            break
    a=input()
    i=0
    p=a[i]
    l1=[]
    while(i<len(a)):
        temp=1
        t=[p]
        i+=1
        while(i<len(a)):
            if a[i]!=p:
                p=a[i]
                break
            p=a[i]
            t.append(p)
            i+=1
            if i==len(a):
                temp=0
                break
        l1.append(t)
        if temp==0:
            break
    if len(l)!=len(l1):
        return 0
    for i in range(0,len(l)):
        if l[i][0]!=l1[i][0] or len(l[i])>len(l1[i]):
            return 0
    return 1

        
        
for i in range(int(input())):
    if f():
        print ("YES")
    else:
        print("NO")
    