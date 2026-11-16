import sys
input=sys.stdin.readline
s=input().rstrip()
n=len(s)
ans=[""]*n
c={}
for i in range(n):
    c[s[i]]=c.get(s[i],0)+1
idx=0
l=[]
for i in range(26):
    al=chr(ord("a")+i)
    if al in c:
        while c[al]-2>=0:
            ans[idx]=ans[n-1-idx]=al
            c[al]-=2
            idx+=1
        if c[al]==1:
            l.append(al)
            c[al]-=1
l.sort(reverse=True)
while idx<=(n-1)//2:
    al=l.pop()
    ans[idx]=ans[n-1-idx]=al
    idx+=1
if n%2==0:
    ans=sorted(ans[:n//2])
    print("".join(ans+ans[::-1]))
else:
    ans1=sorted(ans[:n//2])
    print("".join(ans1+[ans[n//2]]+ans1[::-1]))