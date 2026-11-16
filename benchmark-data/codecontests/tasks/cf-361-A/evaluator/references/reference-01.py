n, p = map(int, input().split())

for i in range(n):
    arr = []
    for j in range(n):
        arr.append("0")
    arr[i] = str(p)
    answer = " ".join(arr)
    print(answer)