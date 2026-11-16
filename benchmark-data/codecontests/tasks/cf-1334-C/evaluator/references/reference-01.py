from sys import stdin, stdout
import io, os
input = stdin.buffer.readline

def inp():
    return int(input())
def arrinp():
    return [int(x) for x in input().split()]
l = []
def main():
    t = inp()
    for _ in range(t):
        n = inp()
        A, B = zip(*[list(map(int, input().split())) for i in range(n)])
        ans, min_cost = 0, float('inf')
        for i in range(n):
            ans += max(A[i] - B[i-1], 0)
            min_cost = min(min_cost, A[i] - max(0, A[i] - B[i-1]))
        l.append(str(min_cost+ans)+"\n")
    stdout.writelines(l)
if __name__ == '__main__':
    main()