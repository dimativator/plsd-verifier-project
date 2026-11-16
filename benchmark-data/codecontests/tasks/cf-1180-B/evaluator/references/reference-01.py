n=int(input())
list1=[*map(int,input().split())]
list2=[]
if n%2==0:
    for element in list1:
        if element>=0:
            print(-element-1)
        else:
            print(element)
else:
    for element in list1:
        if element>=0:
            list2.append(-element-1)
        else:
            list2.append(element)
    index1=list2.index(min(list2))
    for i in range(n):
        if i!=index1:
            print(list2[i],end=" ")
        else :
            print((-list2[i]-1),end=" ")
