for _ in range(int(input())):
    n=int(input())
    a=[]
    b=[0]
    for i in range(50):
        a.append(3**i)
        b.append(b[-1]+a[-1])
        if b[-1]> n:
            break
    s=b[i+1]
    a=a[::-1]
    # print(s,a)

    for j in a:
        if s-j>=n:
            s-=j
    print(s)