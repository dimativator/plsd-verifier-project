n = int(input())
arr = [int(x) for x in input().split()]
for i in range(n):
    while arr[i]%2==0:
        arr[i]/=2
    while arr[i]%3==0:
        arr[i]/=3
print("Yes" if all(arr[0]==arr[i] for i in range(n))else "No")