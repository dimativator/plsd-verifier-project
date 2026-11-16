n, x, y = map(int, input().split())
a = list(map(int,input().split()))

if x > y:
    print( n )
else:
    m = 0
    for i in a:
        if i <= x:
            m += 1
    print( m - m // 2 )
