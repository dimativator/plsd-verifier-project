s=input()
n=len(s)
b=[]
for j in s:
    b.append(j)
x=[]
y=[]
j=0
i=n-1
while(j<i):
    if b[j]==b[i]:
        if i!=j:
            x.append(b[j])
            y.append(b[i])
        else:
            x.append(b[j])
        i+=-1
        j+=1
    elif b[j]==b[i-1]:
        if (i-1) != j:
            x.append(b[j])
            y.append(b[i-1])
        else:
            x.append(b[j])
        j+=1
        i+=-2
    else:
        if b[j+1]==b[i]:
            if i!=(j+1):
                x.append(b[j+1])
                y.append(b[i])
            elif i==(j+1):
                x.append(b[j + 1])
            i+=-1
            j+=2
        else:
            if ((i-1)!= (j + 1)):
                x.append(b[j + 1])
                y.append(b[i-1])
            elif (i-1) == (j + 1):
                x.append(b[j + 1])
            i += -2
            j += 2
res=x+y[::-1]
print("".join(res))

