kl=int(input())
for l in range(kl):
    p=[int(i) for i in input().split()]
    a=min(p[0], p[1])
    b=max(p[0], p[1])
    tn=p[2]-p[3]
    tk=p[2]+p[3]
    if tn>=b or tk<=a:
        print(b-a)
    else:
        if tn>=a:
            print((b-a) - (min(b, tk)-tn))
        else:
            print((b-a) -(min(b, tk)-a))