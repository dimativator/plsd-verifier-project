from collections import *


def add(n):
    for i in range(len(n) - 1, -1, -1):
        if n[i] == '1':
            n[i] = '0'
        else:
            n[i] = '1'
            return n
    n.appendleft('1')
    return n


def main():
    n, ans = deque(input()), 0

    while (len(n) != 1):
        if n[-1] == '1':
            n = add(n)
        else:
            n.pop()
        ans += 1

    print(ans)


if __name__ == '__main__':
    main()
