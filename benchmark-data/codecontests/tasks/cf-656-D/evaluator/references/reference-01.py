n=eval(input())
cnt=0
while n:
    a=n%8
    n=n//8
    if a==1:
        cnt+=1
print(cnt)