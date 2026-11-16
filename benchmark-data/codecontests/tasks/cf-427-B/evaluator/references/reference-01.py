a=list(map(int,input().split()[1:]))
b=list(map(int,input().split()))
m=0
c=0
for i in b:
    if i>a[0]:
        if not c<a[1]:
            m+=c-a[1]+1
        c=0
    else:c+=1
print(m+c-a[1]+1 if c>=a[1]else m)
