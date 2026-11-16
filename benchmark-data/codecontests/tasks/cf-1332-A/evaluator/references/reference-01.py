import sys

I = lambda: int(input())
readline = lambda: sys.stdin.readline().strip('\n')
RM = readmap  = lambda x=int: map(x,readline().split(' '))

#1332 630 div2
for _ in range(I()):
    a,b,c,d,x,y,x1,y1,x2,y2 = *RM(),*RM()
    flag1 = x2-x >= b-a and x-x1 >= a-b and y2-y >= d-c and y-y1 >= c-d
    flag2 = ((b==0 and a==0) or x2-x1>0) and ((c==0 and d==0) or y2-y1>0)
    print(["NO","YES"][flag1 and flag2])



