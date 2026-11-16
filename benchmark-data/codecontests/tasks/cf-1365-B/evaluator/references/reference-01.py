for _ in range(int(input())):
    n=int(input())
    a=list(map(int,input().split()))
    b=list(map(int,input().split()))

    if(sum(b)==0 or sum(b)==n):
        b = sorted(a)
        print('Yes' if a==b else 'No')
    else:
        print('Yes')

