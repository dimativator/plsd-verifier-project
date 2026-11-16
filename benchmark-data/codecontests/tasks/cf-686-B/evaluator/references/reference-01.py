n = int(input())
arr = list(map(int,input().split()))
check = 0
while check==0:
    check = 1
    i = 0
    while i<n-1:
        if arr[i]>arr[i+1]:
            check = 0
            print(i+1,i+2)
            arr[i],arr[i+1] = arr[i+1],arr[i]
        i += 1