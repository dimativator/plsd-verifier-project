# one ride costs a rubes
inputs = list(map(int, input().split()))
x = inputs[0]
y = inputs[1]

if y==0 and 0<=x<=1: print(0)
else:
    a = max(abs(x), abs(y))
    m = 1 + 4*(a-1)
    if x==a and y==-(a-1):print(m-1)
    if x==a and -(a-1)<y<=a: print(m)
    elif y==a and -a<=x<a:print(m+1)
    elif x==-a and -a<=y<a: print(m+2)
    elif y==-a and -a<x<=(a+1):print(m+3)