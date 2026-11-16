n=int(input())
q=list(map(int,input().split()))

eve,eve_indx,neg,neg_indx=0,0,0,0

for i in range(n):
    x=q[i]%2
    if x==0:
        eve +=1
        eve_indx=i
    else:
        neg +=1
        neg_indx=i

if eve==1:
    print(eve_indx+1)
else:
    print(neg_indx+1)