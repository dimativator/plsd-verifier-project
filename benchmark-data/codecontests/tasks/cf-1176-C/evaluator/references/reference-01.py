_=int(input())
a=list(map(int,input().split()))
b=[4,8,15,16,23,42]
c=[0]*6

for i in range(len(a)):
    x = b.index(a[i])
    if x == 0:
        c[0] +=1
    elif c[x-1]!=0:
        c[x-1]-=1
        c[x]+=1
    
print(len(a)-6*c[5])