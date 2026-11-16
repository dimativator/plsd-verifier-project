sum1,sum2,sum3 = 0,0,0
n = int(input())
while n:
    n-=1
    l = list(map(int, input().split()))
    sum1 += l[0]
    sum2 += l[1]
    sum3 += l[2]
if sum1==0 and sum2 ==0 and sum3 ==0:
    print("YES")
else:
    print("NO")