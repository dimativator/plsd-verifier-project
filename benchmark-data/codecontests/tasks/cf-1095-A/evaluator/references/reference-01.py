try:
    t = int(input())
    s = input()
    _ = 1
    i = 0
    l = []
    while((i)<=(len(s)-1)):
        #print(i)
        l.append(s[i])
        _+=1
        i = i+_
    s = "".join(l)  
    print(s)
except:
    pass

