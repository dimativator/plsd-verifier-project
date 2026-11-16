
def intersect(x, y):
    if x < y:
        return (y[0], x[1])
    else:
        return (x[0], y[1])


def solve(iv):
    first = {}
    second = {}
    for x, y in iv:
        first[x] = first.get(x, 0) + 1
        second[y] = second.get(y, 0) + 1
    max1, max2 = reversed(sorted([x for x, _ in iv])[-2:])
    min1, min2 = sorted([y for _, y in iv])[:2]

    res = 0
    for x, y in iv:
        first[x] -= 1
        second[y] -= 1
        if first[x] == 0 and x == max1:
            max_first = max2
        else:
            max_first = max1
        if second[y] == 0 and y == min1:
            min_second = min2
        else:
            min_second = min1
        first[x] += 1
        second[y] += 1
        if min_second - max_first > res:
            res = min_second - max_first
    return res


def main():
    n = int(input())
    iv = []
    for i in range(n):
        a, b = map(int, input().split())
        iv.append((a, b))
    res = solve(iv)
    print(res)


main()
