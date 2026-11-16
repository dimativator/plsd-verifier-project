n= int(input())
for z in range(n):
    h, am = map(int, input().split())
    arr = list(map(int, input().split()))
    ch = h
    i = 1
    ac = 0
    while i < am:
        if ch - arr[i] >= 2:
            ch = arr[i] + 1
        elif i < am - 1 and arr[i + 1] == ch - 2 or ch == 2:
            ch -= 2
            i += 2
        else:
            ch -= 2
            i += 1
            ac += 1
    print(ac)
                    





                
        



