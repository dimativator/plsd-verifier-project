def possible(n, m):
    f = True
    for i in range(n):
        row = list(map(int, input().split()))
        if i == 0 or i == n-1:
            for j in range(m):
                if j == 0 or j == m-1:
                    if row[j] > 2:
                        f = False
                else:
                    if row[j] > 3:
                        f = False
        else:
            for j in range(m):
                if j == 0 or j == m-1:
                    if row[j] > 3:
                        f = False
                else:
                    if row[j] > 4:
                        f = False
    return f


def print_board(n, m):
    for i in range(n):
        if i == 0 or i == n-1:
            for j in range(m):
                if j == 0 or j == m-1:
                    print(2, end=" ")
                else:
                    print(3, end=" ")
        else:
            for j in range(m):
                if j == 0 or j == m-1:
                    print(3, end=" ")
                else:
                    print(4, end=" ")
        print("")


def main():
    n, m = map(int, input().split())
    if possible(n, m):
        print("YES")
        print_board(n, m)
    else:
        print("NO")


for _ in range(int(input())):
    main()