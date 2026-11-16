t=int(input())
for _ in range(t):
    n=int(input())
    s=str(input())
    arr=[]
    for i in range(n):
        arr.append(int(s[i]))
    ones=[]
    zeros=[]
    vals=[]
    k=0
    for i in range(n):
        p=arr[i]
        if(p==0):
            if(ones==[]):
                zeros.append(k+1)
                vals.append(k+1)
                k+=1
            else:
                zeros.append(ones[-1])
                vals.append(ones[-1])
                ones.pop()
        else:
            if(zeros==[]):
                ones.append(k+1)
                vals.append(k+1)
                k+=1
            else:
                ones.append(zeros[-1])
                vals.append(ones[-1])
                zeros.pop()
    print(max(vals))
    for i in vals:
        print(i,end=" ")
    print()

