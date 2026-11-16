t=int(input())
for i in range(t):
    n=int(input())
    l=list(map(int,input().split()))

    d={}
    for i in range(len(l)):
        if l[i] in d:
            d[l[i]].append(i+1)
        else:
            d[l[i]]=[i+1]

    a=[]
    flag=0
    for i in d:
        if len(d[i])==1:
            flag=1
            a.append([i,d[i][0]])
    if flag:
        a.sort();print(a[0][1])
    else:
        print(-1)