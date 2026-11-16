import sys

t=int(sys.stdin.readline())

for _ in range(t):
    a=input()
    a=a[::]
    a=list(map(int, a))
    i=0
    if a.count(0)==0 or a.count(1)==0:
        for j in range(len(a)): 
            print(a[j], end='')
        print()
    else:
        while True:
            if i==len(a)-1:
                break
            if a[i]==0 and a[i+1]==0:
                a.insert(i+1,1)
            elif a[i]==1 and a[i+1]==1:
                a.insert(i+1,0)
            i+=1
        for k in range(len(a)): 
            print(a[k], end='')
        print()