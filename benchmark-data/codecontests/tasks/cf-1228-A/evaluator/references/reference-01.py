l, r =map(int, input().split())
for i in range(l,r+1):
    n = 0
    a = str(i)
    for j in a:
        if a.count(j) == 1:
            n = n+1
        else:
            pass
    if n == len(a):
        break
if n == len(a):
    print(a)
else:
    print('-1')

            
    
    
