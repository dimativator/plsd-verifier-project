T = int(input())

for t in range (T):
    s = input()
    res = ""
    
    for i in range (len(s)):
        if (i%2 == 0):
            if (s[i] == 'a'):
                res += "b"
            else:
                res += "a"
        else:
            if (s[i] == 'z'):
                res += "y"
            else:
                res += "z"
                
    print(res)
            