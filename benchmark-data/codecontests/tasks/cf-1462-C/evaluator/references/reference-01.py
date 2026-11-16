test=int(input())
for testcase in range(test):
    n=int(input())
    if(n<=45):
        if(n<10):
            print(n)
        else:
            i=9
            s=0
            ans=0
            while(i>0):
                #print(i)
                if(s+i<=n):
                    s+=i
                    ans=(ans*10)+i
                    
                if(s>=n):
                    break
                i-=1
                
            if(n==s):
                ans=str(ans)
                print(ans[::-1])
            else:
                print(-1)
    else:
        print(-1)