for i in range(int(input())):
    a,b=input().split()
    if int(b)<=2:
        print("NO")
    elif int(a)%int(b)==0:
        print("YES")
    else:
        print("NO")