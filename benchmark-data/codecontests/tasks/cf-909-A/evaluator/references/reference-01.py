s=input().split(" ")
m=s[0]
j=s[1]
list=[]
for x in range(len(m)):
    p=m[0:x+1]
    p=p+j[0]
    list.append(p)
list.sort()    
print(list[0])