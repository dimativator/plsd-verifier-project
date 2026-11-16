from operator import itemgetter
from collections import defaultdict
n=int(input())
a,b= map(int,input().split())
arr= list(map(int,input().split()))
arr = list(enumerate(arr,0))
arr=sorted(arr,key=itemgetter(1),reverse=True)

def find_min(num1,num2):
    if num1<num2:
        return num1
    else:
        return num2
result=[0]*n


if a==b:
    for i in range(a):
        result[i]=1
    for j in range(a,n):
        if result[j]==0:
            result[j]=2
elif a>b:
    dicta=defaultdict(list)
    for i in range(n):
        dicta[arr[i][1]].append(arr[i][0])
    for j in range(b,n):
        result[dicta[arr[j][1]][0]]=1
        dicta[arr[j][1]].pop(0)
    for k in range(b):
        result[dicta[arr[k][1]][0]]=2
        dicta[arr[k][1]].pop(0)



else:
    min_value= find_min(a,b)
    if min_value==a:
        second_range=b
        val=1
    else:
        second_range=a
        val=2
    for i in range(min_value):
        result[arr[i][0]] = val
    if val==1:
        new_val=2
    else:
        new_val=1
    for j in range(min_value,n):
        result[arr[j][0]]=new_val

for l in result:
    print(l,end=" ")
        






















    # max_arr = arr[n-min_value:]
    # min_arr= arr[:n-min_value]
    # if min_value==a:
    #     for i in max_arr:
    #         result[i[0]]=1
    #     for j in min_arr:
    #         result[j[0]]=2
    #     for k in result:
    #         print(k,end=" ")
    # else:
    #     for i in min_arr:
    #         result[i[0]]=1
    #     for j in max_arr:
    #         result[j[0]]=2
    #     for k in result:
    #         print(k,end=" ")


