def f(x):
    return int(x * x + 1e7)
    
def g(x):
    return -f(x)
    
n, m = map(int, input().split())

if(m == 3):
    if(n == 3):
        print('0 0')
        print('1 0')
        print('0 1')
    elif(n == 4):
        print('0 0')
        print('1 1')
        print('10000 0')
        print('0 10000')
    else:
        print(-1)
else:
    for i in range(m):
        print(i, f(i))
    for i in range(n - m):
        print(i, g(i))