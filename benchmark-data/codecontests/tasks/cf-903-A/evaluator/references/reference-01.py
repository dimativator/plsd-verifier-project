t = int(input())
for i in range(0,t):
    flag = 0
    x = int(input())
    b = 0 
    temp = x
    while temp >= 0 :
        if(temp%3 == 0):
            flag = 1
            break
        b = b+1
        temp = x-7*b
         
    if flag == 1 :
        print("YES")
    else:
        print("NO")
       