s=input().split()

if(len(s)==1):
    if(s[0].endswith("lios") or s[0].endswith("etr") or s[0].endswith("liala") or s[0].endswith("etra") or s[0].endswith("inites") or s[0].endswith("initis")):
        print("YES")
    else:
        print("NO")



elif(s[0].endswith("lios") or s[0].endswith("etr")):
    n=len(s)
    i=0
    while(i<n and s[i].endswith("lios")):
        i+=1
    if(i==n):
        print("NO")
    elif(s[i].endswith("etr")):
        i+=1
        while(i<n and s[i].endswith("initis")):
            i+=1
        if(i==n):
            print("YES")
        else:
            print("NO")
    else:
        print("NO")
        
elif(s[0].endswith("liala") or s[0].endswith("etra")):
    n=len(s)
    i=0
    while(i<n and s[i].endswith("liala")):
        i+=1
    if(i==n):
        print("NO")
    elif(s[i].endswith("etra")):
        i+=1
        while(i<n and s[i].endswith("inites")):
            i+=1
        if(i==n):
            print("YES")
        else:
            print("NO")
    else:
        print("NO")
else:
    print("NO")
    
