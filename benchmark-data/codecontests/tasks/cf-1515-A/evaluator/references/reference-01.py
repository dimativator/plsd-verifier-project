import sys
input = sys.stdin.readline
for i in range(int(input())):
    n,x = map(int,input().split())
    arr = list(map(int,input().split()))
    if sum(arr)==x:
        print("NO")
    else:
        arr.sort()
        print("YES")
        s = 0
        temp = -1
        for i in range(n):
            if s+arr[i]!=x:
                print(arr[i],end = " ")
                s+=arr[i]
            else:
                temp = arr[i]
        if temp!=-1:
            print(temp, end = " ")
        print()
