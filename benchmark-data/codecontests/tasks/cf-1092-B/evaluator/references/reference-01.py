n1=int(input())
s1=list(map(int,input().split()))
s1.sort()
sa1=0
se2=0
for i in range(0,n1,2):
    sa1=sa1+s1[i]
for i in range(1,n1,2):
    se2=se2+s1[i]
print(se2-sa1)