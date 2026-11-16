x=input()
code=x.split()
q=[]
for i in x:
    q.append(i)
code=q
i=0
total=""
while i < len(code):
    if(code[i] == '.'):
        total = total + '0'
    elif(code[i] == '-'):
        if(code[i + 1] == '.'):
            total =total + '1'
        elif (code[i+1] == '-'):
            total = total + '2'
        i+=1
    i=i+1
print(total)