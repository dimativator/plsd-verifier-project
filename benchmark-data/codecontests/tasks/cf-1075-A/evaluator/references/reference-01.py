a=int(input())
n, m=map(int, input().split())
mh=min(abs(1-n),abs(1-m))
mb=min(abs(a-n),abs(a-m))

if mh<=mb:
    print("White")
else:
    print("Black")