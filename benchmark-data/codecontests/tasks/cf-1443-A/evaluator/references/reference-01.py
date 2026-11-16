# cook your dish here
for _ in range(int(input())):
    n=int(input())
    s=4*n-2
    for i in range(n):
        print(s,end=" ")
        s-=2
    print()
