import math
for _  in range(int(input())):
    k=int(input())
    l=list(map(int,input().split()))
    k=sum(l)/k
    print(math.ceil(k))