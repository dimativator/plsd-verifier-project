q=int(input())
for i in range(q):
    n=int(input())
    lst2=[]
    lst1=list(map(int,input().split()))
    for i in range(len(lst1)):
        if lst1[i]<=2048:
            lst2.append(lst1[i])
    sum1=sum(lst2)
    if sum1>=2048:
        print("YES")
    else:
        print("NO")