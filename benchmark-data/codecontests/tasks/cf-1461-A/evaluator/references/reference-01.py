for u in range(int(input())):
    n, k = map(int, input().split())
    t = n-k
    s = ""
    for i in range(t):
        if(i%3==0):
            s += "a"
            
        if(i%3 == 1):
            s += "b"
        
        if(i%3 == 2):
            s += "c"
            
    if(t%3 == 0):
        s += "a"*k
        
    if(t%3 == 1):
        s += "b"*k
        
    if(t%3 == 2):
        s += "c"*k
        
    print(s)