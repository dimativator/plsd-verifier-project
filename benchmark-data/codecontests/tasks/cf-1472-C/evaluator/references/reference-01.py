for _ in range(int(input())):
    n = int(input())
    array = list(map(int, input().split()))
    for i in range(n-1, -1, -1):
        if i+array[i]<=n-1:
            array[i] += array[i+array[i]]
    print(max(array))