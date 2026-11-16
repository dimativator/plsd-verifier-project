from math import log2
for i in range(int(input())):
    K,N=map(int,input().split())
    L=list(map(int,input().split()))
    bit=[0]*61
    Sum=0
    for i in L:
        bit[int(log2(i))]+=1
        Sum+=i
    if Sum<K:
        print("-1")
        continue
    i=0
    res=0
    while i<60:
        if (1<<i)&K!=0:
            if bit[i]>0:
                bit[i]-=1
            else:
                while i<60 and bit[i]==0:
                    res+=1
                    i+=1
                bit[i]-=1
                continue
        bit[i+1]+=bit[i]//2
        i+=1
    print(res)