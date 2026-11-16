n, m = map(int, input().split())
s = [[0] * n for i in range(n)]
for i in range(m):
    a, b = map(int, input().split())
    s[a - 1][b - 1] = 1
    s[b - 1][a - 1] = 1
for i in range(n):
    s[i][i] = 1
answer = [0] * n
for i in range(n):
    flag = True 
    for j in range(n):
        if s[i][j] == 0:
            flag = False
    if flag:
        answer[i] = 'b'
for i in range(n):
    if answer[i] == 0:
        answer[i] = 'a'
        for j in range(n):
            if s[i][j] == 0:
                answer[j] = 'c'
            if s[i][j] == 1 and answer[j] != 'b':
                answer[j] = 'a'
        break
flag = True
for i in range(n):
    for j in range(n):
        if s[i][j] == 1:
            if (answer[i] == 'a' and answer[j] == 'c') or (answer[i] == 'c' and answer[j] == 'a'):
                flag = False
        if s[i][j] == 0:
            if abs(ord(answer[i]) - ord(answer[j])) < 2:
                flag = False
if flag:
    print('Yes')
    answer = ''.join(answer)
    print(answer)
else:
    print("No")
