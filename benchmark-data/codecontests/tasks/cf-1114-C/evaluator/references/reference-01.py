import math
from collections import Counter
def checkprime(x):
    if x==1:
        return False
    i=2
    while i*i<=x:
        if x%i==0:
            return False
        i+=1
    return True
def pfactors(n):
    lt=[]
    while n % 2 == 0:
        lt.append(2)
        n = (n // 2)
    for i in range(3,int(math.sqrt(n))+1,2):       
        while n % i== 0: 
            lt.append(i)
            n = (n//i)
    if n > 2: 
        lt.append(n)
    return lt
def sum(no,bs):
    d=(no//bs)
    #print (d,no%bs)
    s=0
    while d!=0:
        s+=d
        d=(d//bs)
        #print (d,no%bs)
    return s

s=input("")
l=list(map(int,s.split()))
n,b=l[0],l[1]
if checkprime(b)==True:
    print (sum(n,b))
else:
    new1=pfactors(b)
    nd=Counter(new1)
    dd={}
    for i in nd.keys():
        dd[i]=sum(n,i)
    newbb=min(j//nd[i] for i,j in dd.items())
    print(newbb)
