x = int(input())
v = list(map(int,input().strip().split()))[:x]
i = 0
j = x-1
s1 = 0
s2 = 0
ans = 0
while(i<=j):
    if(s2<s1):
       s2+=v[j]
       j=j-1
    else:
        s1+=v[i]
        i=i+1
    if(s1==s2):
        ans=s1
print(ans)