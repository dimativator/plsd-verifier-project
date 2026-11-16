x = int(input())
for i in range(x):
    n, k, d = map(int, input().split(' '))
    l = map(int, input().split(' '))
    l = list(l)
    ar = []
    for j in range(n-d+1):
        ar.append(len(set(l[j:(j+d)])))
    print(min(ar))