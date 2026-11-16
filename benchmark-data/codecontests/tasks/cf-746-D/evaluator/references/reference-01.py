n,k,a,b = [int(i) for i in input().split()]
check = False
if (a>b):
    a,b = b,a
    check = True
res = ""
cr = 1

cA = True

while (a > 0 or b > 0):
    if (a==b):
        break
    #print(a,b)
    if (cr==1):
        if a <= b:
            u = min(k, b - a)
            b -= u
            res += u * '1'
        else:
            if (b==0):
                cA = False
                break
            else:
                b -= 1
                res += '1'
        cr = 0
    else:
        if a >= b:
            u = min(k, a - b)
            a -= u
            res += u * '0'
        else:
            if (a==0):
                cA = False
                break
            else:
                a -= 1
                res += '0'
        cr = 1

if (a==b):
    if (len(res)>0):
        if (res[len(res)-1] =='0'):
            res += '10' * a
        else:
            res += '01' * a
    else:
        res += '01' * a
    

if (b==0 and a > k):
    cA = False
if (a==0 and b > k):
    cA = False

if cA == False:
    print("NO")
else:
    if (check):
        for i in res:
            if i == '1':
                print('G', end ='')
            else:
                print('B', end ='')
    else:
        for i in res:
            if i == '1':
                print('B', end ='')
            else:
                print('G', end ='')
    
            
            
        
