if __name__ == "__main__":
    _ = int(input())
    arr = [int(num) for num in input().split()]
    for i in arr:
        if i % 2 == 0:
            print(i - 1, end=" ")
        else:
            print(i, end=" ")
