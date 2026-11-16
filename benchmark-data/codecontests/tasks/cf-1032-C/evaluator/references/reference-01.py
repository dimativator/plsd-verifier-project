n = int(input())
u = list(map(int, input().split()))
d = []
for i in range(5):
    d.append([0] * n)
for i in range(5):
    d[i][0] = 1
for i in range(1, n):
    if u[i] == u[i - 1]:
        s1 = 0
        for j in range(5):
            if d[j][i - 1] == 1:
                s1 += 1
        if s1 > 1:
            for j in range(5):
                d[j][i] = 1
        else:
            for j in range(5):
                if d[j][i - 1] != 1:
                    d[j][i] = 1
    elif u[i] < u[i - 1]:
        k = 4
        while d[k][i - 1] == 0:
            k -= 1
        for j in range(k):
            d[j][i] = 1
    else:
        k = 0
        while d[k][i - 1] == 0:
            k += 1
        for j in range(k + 1, 5):
            d[j][i] = 1
    ok = True
    for j in range(5):
        if d[j][i] == 1:
            ok = False
            break
    if ok:
        print(-1)
        exit()
k = 4
while d[k][-1] == 0:
    k -= 1
ans = [k + 1]
for i in range(n - 1, 0, -1):
    if u[i] == u[i - 1]:
        for j in range(5):
            if d[j][i - 1] == 1 and j != k:
                k = j
                break
    elif u[i] > u[i - 1]:
        for j in range(k):
            if d[j][i - 1] == 1:
                k = j
                break
    else:
        for j in range(k + 1, 5):
            if d[j][i - 1] == 1:
                k = j
                break
    ans.append(k + 1)
ans.reverse()
print(' '.join(map(str, ans)))





        
