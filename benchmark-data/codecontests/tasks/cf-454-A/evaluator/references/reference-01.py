n=int(input())
a=int(n/2)
b=1
for i in range(int(n/2)):
    for j in range(a):
        print("*",end="")
    for j in range(b):
        print('D',end="")
    b=b+2
    for j in range(a):
        print("*",end="")
    a=a-1
    print()
for i in range(b):
    print("D",end="")
print()
a=a+1
b=b-2
for i in range(int(n/2)):
    for j in range(a):
        print("*",end="")
    for j in range(b):
        print('D',end="")
    b=b-2
    for j in range(a):
        print("*",end="")
    a=a+1
    print()
