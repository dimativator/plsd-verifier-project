for _ in range(int(input())):
    x=input()[::-1]
    y=input()[::-1]
    posy=y.index('1')
    posx=x.index('1',posy)
    print(posx-posy)        
