t = int(input())

for _ in range(t):
    variables = [int(_) for _ in input().split()]
    n = variables[0]
    s = variables[1]
    k = variables[2]
    closed = set([int(i) for i in input().split()])
    minimum = n
    tmp = n
    for x in range(s, 0, -1):
        if x not in closed:
            tmp = abs(s-x)
            if tmp < minimum:
                minimum = tmp
            break
    for x in range(s, n+1):
        if x not in closed:
            tmp = abs(s-x)
            if tmp < minimum:
                minimum = tmp
            break

    print(minimum)