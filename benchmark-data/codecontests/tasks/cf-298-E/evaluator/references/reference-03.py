n=int(raw_input())
s=[int(x) for x in raw_input().split()]
o=[i for i in range(n)]
o=sorted(o,key=lambda x: s[x])
a=[i for i in range(n)]
b=[i for i in range(n)]
k=n/3
for i in range(k):
    j=o[i]
    a[j],b[j]=i,s[j]-i
for i in range((2*n)/3-n/3):
    j=o[k+i]
    a[j],b[j]=s[j]-k-i,k+i
for i in range(n-(2*n)/3):
    j=o[n-1-i]
    b[j]=i
    a[j]=s[j]-b[j]
print "YES"
print " ".join(map(str,a))
print " ".join(map(str,b))