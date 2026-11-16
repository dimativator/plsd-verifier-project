# cook your dish here
#import sys
#sys.setrecursionlimit(10**9) 
ll=lambda:map(int,input().split())
t=lambda:int(input())
ss=lambda:input()
lx=lambda x:map(int,input().split(x))
yy=lambda:print("YES")
nn=lambda:print("NO")

from math import log10 ,log2,ceil,factorial as fac,gcd,inf,sqrt,log
#from itertools import combinations_with_replacement as cs 
#from functools import reduce
from bisect import bisect_right as br,bisect_left as bl
from collections import Counter
#from math import inf


mod=10**9+7


            
#for _ in range(t()):
def f():
    
    
    n,m=ll()
    a=list(ll())
    s=ss()

    su=0
    i=0
    while i<n:
        temp=[a[i]]
        for j in range(i,n-1):
            if s[j+1]==s[j]:
                temp.append(a[j+1])
    
            else:
                i=j+1
                break
        else:
            i=n
        #print(i,s[i],temp,su,j)
        
        
        temp.sort(reverse=1)
        su+=sum(temp[:m])
    print(su)
    
        
        
                
    
    
    
                
        
    
f()
    

'''

baca

bac
1 2 3
baaccca

abbaccccaba
 
'''
