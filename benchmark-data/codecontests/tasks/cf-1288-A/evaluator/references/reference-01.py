import math
for _ in range(int(input())):
    n,d = map(int,input().split())


    if ((1-n)**2) - (4*(d-n)) >= 0:
        print('YES')
    else:
        print('NO')
    
    
