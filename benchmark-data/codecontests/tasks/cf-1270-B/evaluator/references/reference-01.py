def findsubarray(n,ll):
    for i in range(0,n-1):
        if abs(ll[i]-ll[i+1])>1:
            return 1,i+1,i+2
    return 0,None,None
        
tests = int(input())
for i in range(0,tests):
    numberlen = int(input())
    numbers = input().split()
    numberss = list(map(int,numbers))
    result, left,right = findsubarray(numberlen, numberss)
    if result>0:
        print("YES")
        print(str(left)+' '+str(right))
    else:
        print("NO")