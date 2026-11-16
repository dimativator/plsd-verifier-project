from collections import Counter
n=int(input())
a=[]
for i in range(n):
    a.append(list(map(int,input().split())))
#a.append(a[0])
m=10000000000
for i in range(-1,n-1):
    b=a[i+1][0]-a[i-1][0]
    c=a[i-1][1]-a[i+1][1]
    d=-a[i-1][1]*b-a[i-1][0]*c
    m=min(m,((a[i-1][0]-a[i][0])**2+(a[i-1][1]-a[i][1])**2)**0.5,\
          ((a[i+1][0]-a[i][0])**2+(a[i+1][1]-a[i][1])**2)**0.5,\
          abs(b*a[i][1]+\
              c*a[i][0]+\
              d)/(b**2+c**2)**0.5)
print(m/2)


