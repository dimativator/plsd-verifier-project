from math import ceil

n=int(input())
reports = list(map(int,input().split()))
k=0
count=0
lst=[]
for i in reports:
    count += 1
    if i<0:
        if k+1 > 2:
            lst.append(count-1)
            count=1
            k=1
        else:
            k+=1
lst.append(count)
print(len(lst))
for i in lst:
    print(i,end=' ')


