from sys import stdin, stdout
from collections import deque


def main():
    t = int(stdin.readline())
    for _ in range(t):
        n = int(stdin.readline())
        ar = deque(map(int, stdin.readline().split()))
        a = 0
        b = 0
        prev = ar.popleft()
        a += prev
        turn = 1
        move = 1
        while ar:
            if turn == 1:
                curr = 0
                while ar and curr <= prev:
                    curr += ar.pop()
                b += curr
                prev = curr
                move += 1
            else:
                curr = 0
                while ar and curr <= prev:
                    curr += ar.popleft()
                a += curr
                prev = curr
                move += 1
            turn = 1 - turn
        print(move, a, b)


if __name__ == "__main__":
    main()
