from sys import stdin

def count(N, l, r):
    resultmin, resultmax = 0, 0
    fmax, smax = 1, 1
    for n in range(N):
        if l:
            resultmin += fmax
            fmax *= 2
            l -= 1
        else:
            resultmin += 1
        if r:
            resultmax += smax
            smax *= 2
            r -= 1
        else:
            resultmax += smax//2
    return resultmin, resultmax

def main():
    num = list(map(int, stdin.readline().split()))
    result = count(num[0], num[1], num[2])
    print(result[0], result[1])
    return

main()
