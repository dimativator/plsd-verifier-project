for x in range(int(input())):
    n = int(input())
    s = input()
    if s[0]+s[1]+s[2]+s[3] == "2020":
        print("YES")
    elif s[0]+s[1]+s[2]+s[n-1] == "2020":
        print("YES")
    elif s[0]+s[1]+s[n-2]+s[n-1] == "2020":
        print("YES")
    elif s[0]+s[n-3]+s[n-2]+s[n-1] == "2020":
        print("YES")
    elif s[n-4]+s[n-3]+s[n-2]+s[n-1] == "2020":
        print("YES")
    else:
        print("NO")