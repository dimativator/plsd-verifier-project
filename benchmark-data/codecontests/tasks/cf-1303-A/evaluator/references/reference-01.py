n=int(input())
for i in range(n):
    x=input()
    if '1' in x:
        a=x.index('1')
        c=0
        for j in range(a+1,len(x)):
            if x[j]=='1':
                c+=x.count('0',a,j)
                a=j
        print(c)
    else:
        print(0)