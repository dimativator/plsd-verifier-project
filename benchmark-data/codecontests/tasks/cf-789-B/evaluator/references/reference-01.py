b1,q,l,m = map(int,input().split())
a = set(map(int,input().split()))
if q==0:
    if 0 in a:
        if b1 in a:
            print(0)
        elif abs(b1)<=l:
            print(1)
        else:
            print(0)
    elif abs(b1)<=l:
        print("inf")
    else:
        print(0)
elif q==1:
    if abs(b1)<=l and b1 not in a:
        print("inf")
    else:
        print(0)
elif q==-1:
    if abs(b1)<=l and (b1 not in a or -b1 not in a):
        print('inf')
    else:
        print(0)
elif b1==0:
    if 0 in a:
        print(0)
    else:
        print("inf")
else:
    cnt = 0
    p = b1
    while abs(p)<=l:
        if p not in a:
            cnt += 1
        p *= q
    print(cnt)