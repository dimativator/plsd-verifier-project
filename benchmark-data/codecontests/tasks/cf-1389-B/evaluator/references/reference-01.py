# Some people dream of success, while others wake up and work hard at it. Napoleon Hill
# by : Blue Edge - Create some chaos

# import sys
# sys.stdin = open('input.txt', 'r')

for _ in range(int(input())):
    n,k,z=map(int,input().split())
    a=list(map(int,input().split()))
    # print(k,z)
    # print(*a)
    s=[0]
    for x in a:
        s+=x+s[-1],
    # print(*s)

    ans=0
    i=0
    ans=0
    while i<k:
        sum = s[i+1]-s[0]
        # print(sum,end=" ")
        mv = k-i
        hf = mv//2
        l = min(z,hf)
        sum += l*(a[i]+a[i+1])
        mv-=2*l
        if mv:
            sum+=s[i+1+mv]-s[i+1]
        # print(sum)
        ans = max(sum,ans)
        i+=1
    print(ans)
