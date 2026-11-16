for _ in range(int(input())):
    bool = True
    n, h = map(int, input().split())
    list = [int(x) for x in input().split()]
    maxi, mini = list[0], list[0]
    for i in range(1, n):
        maxi = max(maxi - h + 1, list[i])
        mini = min(mini + h - 1, list[i] + h - 1)
        if maxi > mini:
            bool = False
    if maxi != list[-1]:
        bool = False
    print("NO") if bool == False else print("YES")
