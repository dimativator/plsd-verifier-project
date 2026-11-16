n,m=map(int,input().split())
s="."*(m-1)+"#"
#print(s)
for i in range(n):
    if i%2==0:print("#"*m)
    else:
        print(s)
        s=s[::-1]