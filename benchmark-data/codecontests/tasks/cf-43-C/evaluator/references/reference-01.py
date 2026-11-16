n=int(input())
inp = list(map(int,input().split()))
l=[0,0,0]
for item in inp:
    l[item%3]+=1
a=l[0]
b=l[1]
c=l[2]
print (min(b,c)+a//2)