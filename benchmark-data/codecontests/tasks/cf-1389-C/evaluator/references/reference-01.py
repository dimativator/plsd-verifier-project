t = int(input())
for i in range(t):
    s=input()
    ans=0
    e=len(s)
    qr=0
    for j in range(10):
        for q in range(10):
            b=False
            r=0
            for i in range(len(s)):
                if j!=q:
                    
                    if (s[i]==str(j)) and (not b):
                        b=True
                        r+=1
                    if (s[i]==str(q)) and b:
                        b=False
                        r+=1
                else:
                    if s[i]==str(j):
                        r+=1
                   
                   
                   

            
            if j==q:
                ans=max(ans,r)
            else:
                r=r-r%2
                ans=max(ans,r)
    print(e-ans)

    


    
        
