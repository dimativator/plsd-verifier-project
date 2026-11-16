#from math import pow
def pow(num, n):
    ans = 1
    while n>0:
        ans*=num
        n-=1
    return ans
l,r,k = map(int, input().split())
i = 0;
while (pow(k,i)<l):
    i+=1
    
count = 0
a = []
while (l<=pow(k,i)<=r):
    a.append(int(pow(k,i)))
    count += 1
    i+=1

if count == 0:
    print(-1)
else:
    for i in range(count):
        print(a[i], end=" ")
