for _ in range(int(input())):
    arr=list(input())
    n=len(arr)
    fix=1;mis=0;plus=0
    ans=0
    for i in range(n):
        if(arr[i]=="-"):
            if(plus>0):
                plus-=1
                continue
            else:
                ans+=(i+1)
        if(arr[i]=="+"):
            plus+=1
            continue
    ans+=n
    print(ans)