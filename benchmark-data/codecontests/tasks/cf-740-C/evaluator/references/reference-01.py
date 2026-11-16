n,m=map(int,input().split())
min_val=9999999
for _ in range(m):
    y,x=map(int,input().split())
    if min_val>x-y:
        x1=x
        y1=y
        min_val=x-y
print(min_val+1)
L=[0]*n
tp=0
listNum=[]
for i in range(n):
    listNum.append(tp)
    tp+=1
    if tp>min_val:
        tp=0
for i in listNum[:-1]:
    print(i,end=' ')
print(listNum[-1])