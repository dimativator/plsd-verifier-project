# cook your dish here
n=int(input())
s=list(input())*n
d={}
for i in range(len(s)):
    if s[i] not in d:
        d[s[i]]=[i]
    else:
        d[s[i]].append(i)
m=int(input())
for i in range(m):
    o,c=input().split()
    s[d[c].pop(int(o)-1)]=''
print(''.join(s))