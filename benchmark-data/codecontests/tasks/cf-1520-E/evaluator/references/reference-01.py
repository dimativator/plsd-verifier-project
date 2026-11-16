t=int(input())
for i in range(t):
    n=int(input())
    s=input();y=0;b=[]
    for i in range(n):
        if s[i]=='*':y+=1;b.append(i)

    x=y//2
    if len(b)==n or len(b)==0 or len(b)==1 : print(0)
    else:
        moves=0
        for i in range(len(b)):
            moves+=abs(abs(b[x]-b[i]-1)-abs(x-i-1))
        print(moves)