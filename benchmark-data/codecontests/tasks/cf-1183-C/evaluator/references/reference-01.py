n=int(input())
for i in range(0,n):
    p=input().rstrip().split(' ')
    k=int(p[0])
    K=k;
    n=int(p[1])
    CC=n;
    a=int(p[2])
    b=int(p[3])
    T=min(a,b);
    if (k%T==0):
        H=(k//T)-1;
    else:
        H=(k//T)
    if n>H:
        print(-1)
    else:
        if k%a==0:
            A=(k//a)-1;
        else:
            A=(k//a)
        B=k-(A*a)
        k=B;
        n=n-A;
        if n<=0:
            if A>=CC:
                print(CC)
            else:
                print(A)
        else:
            G=(b*n);
            if k>G:
                if A>=CC:
                    print(CC)
                else:
                    print(A)
            else:
                V=-99999;
                GG=1;
                MM=G-k;
                LL=a-b;
                XX=(MM//LL)+1;
                A=A-XX;
                if A>=CC:
                    print(CC)
                else:
                    print(A)
