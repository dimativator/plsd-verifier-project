import sys
from collections import *
from fractions import gcd
nok=lambda x,y: x*y/gcd(x,y)
def fail():
    print "NO"
    sys.exit(0)
n,m = map(int,raw_input().split())
r = [map(int,raw_input().split()) for i in xrange(m)]
a0 = [1]*n
aa = [1]*n
for x,y,nd,nk in r:
    a0[x-1]=nok(a0[x-1],nd)
    a0[y-1]=nok(a0[y-1],nd)
rl = [[] for i in range(n)]    
for x,y,nd,nk in r:
    kk= nok(a0[x-1],a0[y-1])    
    if nk%kk != 0: fail()
    kk = nk/kk
    rl[x-1].append((y-1,kk,nd))
    rl[y-1].append((x-1,kk,nd))
f = [False]*n
for i in xrange(n):
    if f[i]: continue
    lk = [k for v,k,kd in rl[i]]
    no = reduce(gcd,lk) if lk else 1
    fl = False
    for k in range(1,no+1):
        if no%k!=0: continue
        a = [i]        
        f[i]=True
        aa[i]=k
        fl = True
        for v in a:        
            vk = aa[v]
            for nv,nk,nd in rl[v]:                    
                if nk%vk != 0:
                    fl=False
                    break
                rk = nk/vk
                if f[nv]:
                    if rk!=aa[nv]: 
                        fl=False
                        break
                else:                    
                    if gcd(a0[nv]*rk,vk*a0[v])>nd:
                        fl=False
                        break                        
                    f[nv]=True
                    aa[nv]=rk
                    a.append(nv)
        if fl: 
            break
        for k in a: f[k]=False
    if not fl: fail()
print "YES"
print ' '.join(map(lambda a,b: str(a*b),a0,aa))